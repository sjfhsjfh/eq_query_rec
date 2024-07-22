from tqdm import tqdm
from model import Equation
from pathlib import Path
from query import query_eq
from typing import List
from fix_physica import fix_physica

def main(root):
    root = Path(root)
    if not root.exists():
        root.mkdir()

    res: List[Equation] = []

    for typ in tqdm(
            root.glob("**/*.typ"),
            desc="Files compiled",
            unit="file",
            total=len(list(root.glob("**/*.typ")))
    ):
        res.extend(query_eq(typ, root=root))
    import json
    with open(root / "out.json", "w") as f:
        json.dump(
            [r.reconstruct() for r in tqdm(
                res,
                desc="Standardizing equations",
                unit="eq",
                total=len(res)
            )],
            f,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":
    root = Path(".")
    fix_physica()
    main(root)
    fix_physica()
