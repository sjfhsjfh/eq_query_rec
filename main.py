from typing import List
from model import Equation
from query import query_eq


def main(root):
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
    from pathlib import Path
    root = Path(__file__).parent
    main(root / "test")
