from .query import query_eq
import pandas as pd
import concurrent.futures
import hashlib
import os
import csv

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
    return normalized_eq


def process_row(row):
    try:
        original_value = row[1]
        normalized_value = normalize(original_value)[2:-2]
        return row[0], normalized_value, None
    except Exception as e:
        return row[0], None, row[1]


def normalize_csv_column(csv_path):
    if not (os.path.exists("tmp/") and os.path.isdir("tmp/")):
        os.makedirs("tmp")

    failed_rows = []
    normalized_csv_path = f"{os.path.dirname(csv_path)}/normalized_{os.path.basename()}"

    with open(csv_path, "r", newline="", encoding="utf-8") as infile, open(
        normalized_csv_path, "w", newline="", encoding="utf-8"
    ) as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        writer.writerow(headers)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_row, row): row for row in reader}
            for future in concurrent.futures.as_completed(futures):
                index, normalized_value, error = future.result()
                if normalized_value is not None:
                    writer.writerow([index, normalized_value])
                if error is not None:
                    failed_rows.append((index, error))

    if failed_rows:
        with open("normalize_failed.txt", "w") as f:
            for index, failed_row in failed_rows:
                f.write(f"Index {index}: {failed_row}\n")
