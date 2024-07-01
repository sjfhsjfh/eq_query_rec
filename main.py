from typing import List
from model import Equation
from query import query_eq
from pathlib import Path


def main(root):
    root = Path(root)
    if not root.exists():
        root.mkdir()

    res: List[Equation] = []
    for typ in root.glob("**/*.typ"):
        try:
            res.extend(query_eq(typ, root=root))
        except Exception as e:
            print(f"Error: {e}")
    import json
    with open(root / "out.json", "w") as f:
        json.dump([r.reconstruct()
                  for r in res], f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root = Path(__file__).parent
    main(root / "test")
