from __future__ import annotations
from typing import Dict, List, Optional

from .objects.accent import Accent
from .objects.cancel import Cancel
from .objects.class_ import Class
from .objects.equation import Equation
from .objects.text import Text
from .objects.overline import Overline
from .objects.underline import Underline
from .objects.overbrace import Overbrace
from .objects.underbrace import Underbrace
from .objects.overbracket import Overbracket
from .objects.underbracket import Underbracket
from .objects.mid import Mid
from .objects.limits import Limits
from .objects.scripts import Scripts
from .objects.lr import LR
from .objects.space import Space
from .objects.alignpoint import AlignPoint
from .objects.frac import Frac
from .objects.binom import Binom
from .objects.cases import Cases
from .objects.vec import Vec
from .objects.primes import Primes
from .objects.linebreak import LineBreak
from .objects.matrix import Matrix
from .objects.root import Root
from .objects.h import H
from .objects.move import Move
from .objects.attach import Attach
from .objects.op import Op
from .objects.styled import Styled
from .objects.strike import Strike
from .objects.sequence import Sequence


def escape(s: str, chars: str = "\\,;.$&#\"'") -> str:
    """
    Single character escape
    """
    assert len(s) == 1
    if s in chars:
        return "\\" + s
    return s


def func_recon(name, *args, **kwargs):
    # Remove No
    # ne values in kwargs
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    def to_str(x):
        if isinstance(x, TypstObj):
            return x.reconstruct(chars="\\.$&#\"'")

    arg_items = list(map(lambda x: f"{x[0]}: {to_str(x[1])}", kwargs.items()))
    arg_items.extend(list(map(str, args)))
    return f"{name}( {', '.join(arg_items)} )"


class TypstObj:
    """
    Typst Obj, in json its
    ```json
    {
        "func": "xxx"
        "arg_1": "val_1"
        ...
    }
    ```
"""

    def __init__(self, func: str, *args, **kwargs) -> None:
        self.func = func
        self.args = args

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return self.reconstruct()

    def __repr__(self) -> str:
        res = self.__dict__
        PROTECTED = []
        for p in PROTECTED:
            res.pop(p)
        s = f"{self.func}({', '.join([f'{k}: {v}' for k, v in res.items()])})"
        return s

    @classmethod
    def from_dict(cls, d: dict) -> TypstObj:
        raise NotImplementedError

    def reconstruct(self, chars="\\,;.$&#\"'") -> str:
        for k, v in CONSTS.items():
            if v.__eq__(self):
                return f"{k}"
        raise NotImplementedError


SKIP = (
    "box",
    "context",
    "grid",
    # "move",
    "(..) => ..",  # wtf is this
)


def from_dict(d: dict, break_equation: bool = True) -> TypstObj:
    if d["func"] == "equation":
        if break_equation:
            return Equation(**d).body
        return Equation(**d)
    if d["func"] == "overline":
        return Overline(**d)
    if d["func"] == "underline":
        return Underline(**d)
    if d["func"] == "overbrace":
        return Overbrace(**d)
    if d["func"] == "underbrace":
        return Underbrace(**d)
    if d["func"] == "overbracket":
        return Overbracket(**d)
    if d["func"] == "underbracket":
        return Underbracket(**d)
    if d["func"] == "mid":
        return Mid(**d)
    if d["func"] == "limits":
        return Limits(**d)
    if d["func"] == "scripts":
        return Scripts(**d)
    if d["func"] == "cancel":
        return Cancel(**d)
    if d["func"] == "accent":
        return Accent(**d)
    if d["func"] == "class":
        return Class(**d)
    if d["func"] == "sequence":
        return Sequence(**d)
    if d["func"] == "cases":
        return Cases(**d)
    if d["func"] == "vec":
        return Vec(**d)
    if d["func"] == "mat":
        return Matrix(**d)
    if d["func"] == "text":
        return Text(**d)
    if d["func"] == "lr":
        return LR(**d)
    if d["func"] == "space":
        return Space(**d)
    if d["func"] == "primes":
        return Primes(**d)
    if d["func"] == "linebreak":
        return LineBreak(**d)
    if d["func"] == "align-point":
        return AlignPoint(**d)
    if d["func"] == "frac":
        return Frac(**d)
    if d["func"] == "binom":
        return Binom(**d)
    if d["func"] == "root":
        return Root(**d)
    if d["func"] == "attach":
        return Attach(**d)
    if d["func"] == "h":
        return H(**d)
    if d["func"] == "styled":
        return Styled(**d)
    if d["func"] == "op":
        return Op(**d)
    if d["func"] == "move":
        return Move(**d)
    if d["func"] == "strike":
        return Strike(**d)

    if d["func"] in SKIP:
        # Ignore
        # print(f"Skipping {d['func']}")
        return Space(func="space")
    print(d)
    raise ValueError(f"Invalid TypstObj {d['func']}")


CONSTS: Dict[str, TypstObj] = {}
"""Human-readable shorthand, reading from `const.json`"""

CONST_KMP: Dict[str, List[int]] = {}
"""KMP table for each CONSTS"""


def load_consts(fp="const.merged.typ"):
    global CONSTS, CONST_KMP
    from pathlib import Path
    import json
    import typst

    DIR = Path(__file__).parent
    ALL = json.loads(
        typst.query(DIR / fp, selector="math.equation", root=DIR))[0]
    with open(DIR / fp, "r") as f:
        texts = f.readlines()
    texts = map(lambda x: x.strip(), texts)
    texts = filter(lambda x: not x.startswith("$"), texts)
    texts = map(lambda x: x.strip("\\"), texts)
    texts = filter(lambda x: not x.startswith("//"), texts)
    texts = list(texts)
    vals = []
    cur: List[TypstObj] = []
    for child in from_dict(ALL).children:  # type: ignore
        if isinstance(child, Space):
            vals.append(cur)
            cur = []
            continue
        cur.append(child)
    vals.append(cur)
    vals = list(filter(lambda x: x != [], vals))
    assert all(map(lambda x: len(x) == 1, vals))
    assert len(texts) == len(vals)
    CONSTS.update({sc.strip(): vs[0] for sc, vs in zip(texts, vals)})

    # KMP table
    for k, v in CONSTS.items():
        if isinstance(v, Sequence):
            t = [0] * len(v.children)
            j = 0
            for i in range(1, len(v.children)):
                if v.children[i] == v.children[j]:
                    j += 1
                else:
                    j = 0
                t[i] = j
            CONST_KMP[k] = t


ACCENTS = {
    "\u0300": {"callable": True, "name": "grave"},
    "\u0301": {"callable": True, "name": "acute"},
    "\u0302": {"callable": True, "name": "hat"},
    "\u0303": {"callable": True, "name": "tilde"},
    "\u0304": {"callable": True, "name": "macron"},
    "\u2013": {"callable": False, "name:": "dash", "shortcut": "dash"},
    "\u0306": {"callable": True, "name": "breve"},
    "\u0307": {"callable": True, "name": "dot"},
    "\u0308": {"callable": True, "name": "dot.double"},
    "\u20db": {"callable": True, "name": "dot.triple"},
    "\u20dc": {"callable": True, "name": "dot.quad"},
    "\u030a": {"callable": True, "name": "circle"},
    "\u030b": {"callable": True, "name": "acute.double"},
    "\u030c": {"callable": True, "name": "caron"},
    "\u20d6": {"callable": True, "name": "arrow"},
    "\u20d7": {"callable": True, "name": "arrow.l"},
    "\u20e1": {"callable": True, "name": "arrow.l.r"},
    "\u20d0": {"callable": True, "name": "harpoon"},
    "\u20d1": {"callable": True, "name": "harpoon.lt"},
}


load_consts("const.typ")
