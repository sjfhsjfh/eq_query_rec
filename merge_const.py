from query import query_eq
from typing import List

import os

with open("const.typ", "r") as f:
    lines = f.readlines()
    # remove $
    lines = lines[1:-1]

    # remove indent
    lines = [line[2:] for line in lines]


# create typ
temp_file_path = "temp.typ"
with open(temp_file_path, "w") as temp_file:
    for line in lines:
        line = line.strip()
        if not line.startswith("//"):
            temp_file.write(f"$ {line} $\n")


eqs = query_eq(temp_file_path, root=".")
eqs = [eq.body for eq in eqs]


line_eq_map = {}
eq_index = 0
for line in lines:
    line = line.strip()
    if not line.startswith("//"):
        line_eq_map[line] = eqs[eq_index]
        eq_index += 1


# find equivlent consts
processed_eqs = []
for eq in eqs:
    if eq in processed_eqs:
        continue
    processed_eqs.append(eq)

    same_eq_lines = [line for line, line_eq in line_eq_map.items() if line_eq == eq]

    if len(same_eq_lines) > 1:
        print("these consts are equal:")
        for idx, line in enumerate(same_eq_lines):
            print(f"{idx}: {line}")
        user_index = int(input("preferred index: "))
        user_input = same_eq_lines[user_index]

        for line in same_eq_lines:
            index = lines.index(line + "\n")
            lines[index] = f"// {line}\n{user_input}\n  "


with open("const.merged.typ", "w") as f:
    lines = ["  " + line for line in lines]
    lines = ["$", *lines, "$"]
    f.writelines(lines)

os.remove(temp_file_path)
