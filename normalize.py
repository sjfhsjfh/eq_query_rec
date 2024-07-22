from .query import query_eq
import pandas as pd
import concurrent.futures
import hashlib
import os

hashes = set()


def gen_name(eq) -> str:
    original_hash = cur_name = hashlib.md5(eq.encode("utf-8")).hexdigest()
    counter = 1
    while cur_name in hashes:
        cur_name = f"{original_hash}_{counter}"
        counter += 1
    hashes.add(cur_name)
    return cur_name


def normalize(eq):
    temp_file_path = f"tmp/{gen_name(eq)}.typ"
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(f"$ {eq} $")

    trees = query_eq(temp_file_path)

    normalized_eq = trees[0].reconstruct()
    print(normalized_eq)
    return normalized_eq


def process_row(index, row):
    try:
        original_value = row.iloc[1]
        row.iloc[1] = normalize(original_value)[2:-2]
        return index, row, None
    except:
        return index, None, row.iloc[1]


def normalize_csv_column(csv_path):
    df = pd.read_csv(csv_path)

    failed_rows = []
    normalized_rows = [None] * len(df)

    if not (os.path.exists("tmp/") and os.path.isdir("tmp/")):
        os.makedirs("tmp")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(process_row, index, row): index
            for index, row in df.iterrows()
        }
        concurrent.futures.wait(futures)
        for future in concurrent.futures.as_completed(futures):
            index, row, error = future.result()
            if row is not None:
                normalized_rows[index] = row
            if error is not None:
                failed_rows.append(error)

    normalized_rows = [row for row in normalized_rows if row is not None]
    normalized_df = pd.DataFrame(normalized_rows, columns=df.columns)

    normalized_df.to_csv(f"normalized_{csv_path}", index=False)

    if failed_rows:
        with open("normalize_failed.txt", "w") as f:
            for failed_row in failed_rows:
                f.write(f"{failed_row}\n")
