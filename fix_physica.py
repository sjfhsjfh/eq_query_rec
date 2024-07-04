import os
import platform
from pathlib import Path

patches = {
    "0.7.5": [
        {"line_number": 449, "patch": "let dsym = math.dif"},
        {"line_number": 501, "patch": "let d = math.dif"},
    ],
    "0.8.0": [
        {"line_number": 457, "patch": "let dsym = math.dif"},
        {"line_number": 509, "patch": "let d = math.dif"},
    ],
    "0.8.1": [
        {"line_number": 458, "patch": "let dsym = math.dif"},
        {"line_number": 510, "patch": "let d = math.dif"},
    ],
    "0.9.0": [
        {"line_number": 450, "patch": "let dsym = math.dif"},
        {"line_number": 502, "patch": "let d = math.dif"},
    ],
    "0.9.1": [
        {"line_number": 467, "patch": "let dsym = math.dif"},
        {"line_number": 491, "patch": "$#arr.join(prod)$"},
        {"line_number": 525, "patch": "let d = math.dif"},
    ],
    "0.9.2": [
        {"line_number": 550, "patch": "let dsym = math.dif"},
        {"line_number": 574, "patch": "$#arr.join(prod)$"},
        {"line_number": 608, "patch": "let d = math.dif"},
    ],
    "0.9.3": [
        {"line_number": 567, "patch": "let dsym = math.dif"},
        {"line_number": 591, "patch": "$#arr.join(prod)$"},
        {"line_number": 625, "patch": "let d = math.dif"},
    ],
}


def replace_line_in_file(file_path, line_number, new_value):
    original_value = None

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if line_number <= 0 or line_number > len(lines):
        raise IndexError("invalid line number")

    original_value = lines[line_number - 1].rstrip()

    lines[line_number - 1] = new_value + "\n"

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

    return original_value


def get_physica_root():
    system_type = platform.system()

    path = ""

    if system_type == "Linux":
        path = Path(os.path.expanduser("~/.cache"))
    elif system_type == "Darwin":
        path = Path(os.path.expanduser("~/Library/Application Support"))
    elif system_type == "Windows":
        path = Path(os.getenv("APPDATA"))
    else:
        raise OSError("Unsupported operating system")

    return path / "typst" / "packages" / "preview" / "physica"


def fix_physica():
    physica_root = get_physica_root()
    physicas = physica_root.iterdir()

    for physica in physicas:
        for patch in patches[physica.name]:
            patch["patch"] = replace_line_in_file(
                physica / "physica.typ",
                patch["line_number"],
                patch["patch"],
            )

