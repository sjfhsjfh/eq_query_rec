import typst
import json

from model import Equation, from_dict
from typing import List


def query_eq(*args, **kwargs) -> List[Equation]:
    kwargs["format"] = "json"
    kwargs["selector"] = "math.equation"

    ds = json.loads(typst.query(*args, **kwargs))

    def narrow_to_eq(d: dict) -> Equation:
        res = from_dict(d)
        assert isinstance(res, Equation)
        return res
    res = [narrow_to_eq(d) for d in ds]
    return res


if __name__ == "__main__":
    from pathlib import Path
    DIR = Path(__file__).parent
    test = DIR / "test" / "test.typ"
    with open(DIR / "test" / "test.json", "w") as f:
        f.write(typst.query(test, "math.equation", format="json"))
