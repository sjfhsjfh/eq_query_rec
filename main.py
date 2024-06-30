from typing import List
from model import Equation
from query import query_eq

if __name__ == "__main__":
    from pathlib import Path
    DIR = Path(__file__).parent
    test_dir = DIR / "test"
    if not test_dir.exists():
        test_dir.mkdir()

    # Translate all .typ files in test/
    res: List[Equation] = []
    for typ in test_dir.glob("**/*.typ"):
        try:
            res.extend(query_eq(typ, root=DIR))
        except Exception as e:
            print(f"Error: {e}")
    import json
    with open(test_dir / "out.json", "w") as f:
        json.dump([r.reconstruct()
                  for r in res], f, indent=4, ensure_ascii=False)
