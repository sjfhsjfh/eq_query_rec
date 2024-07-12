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
from .objects.cases import Cases
from .objects.vec import Vec
from .objects.primes import Primes
from .objects.linebreak import LineBreak


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


class Sequence(TypstObj):

    def __init__(
        self,
        children: list[dict | TypstObj],
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "sequence":
            raise ValueError("func must be sequence")
        super().__init__(*args, **kwargs)
        self.func = "sequence"
        self.children = [from_dict(child) if isinstance(
            child, dict) else child for child in children]

    def __eq__(self, value: Sequence) -> bool:
        if not isinstance(value, Sequence):
            return False
        if len(self.children) != len(value.children):
            return False
        for a, b in zip(self.children, value.children):
            if not a.__eq__(b):
                return False
        return True

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            def process_slice(s: List[TypstObj]):
                # KMP find Sequence in CONSTS
                for k, v in CONSTS.items():
                    if not isinstance(v, Sequence):
                        continue
                    i = 0
                    j = 0
                    while i < len(s) and j < len(v.children):
                        if s[i] == v.children[j]:
                            i += 1
                            j += 1
                            if j == len(v.children):
                                return process_slice(s[:i - j]) \
                                    + [k] + process_slice(s[i:])
                        else:
                            t = CONST_KMP[k]
                            if j == 0:
                                i += 1
                            else:
                                j = t[j - 1]
                return [c.reconstruct() for c in s]

            return " ".join(process_slice(self.children))


class Matrix(TypstObj):
    def __init__(
        self,
        rows: list[list[dict | TypstObj]],
        delim: str = "(",
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "mat":
            raise ValueError("func must be mat")
        super().__init__(*args, **kwargs)
        self.func = "mat"
        self.delim = delim
        self.rows = [[from_dict(cell) if isinstance(
            cell, dict) else cell for cell in row] for row in rows]

    def __eq__(self, value: Matrix) -> bool:
        if not isinstance(value, Matrix):
            return False
        if self.delim != value.delim:
            return False
        if len(self.rows) != len(value.rows):
            return False
        for a, b in zip(self.rows, value.rows):
            if len(a) != len(b):
                return False
            for c, d in zip(a, b):
                if not c.__eq__(d):
                    return False
        return True

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            rows = []
            for row in self.rows:
                rows.append(", ".join([cell.reconstruct() for cell in row]))
            body = '; '.join(rows)
            if self.delim == "(" or self.delim is None:
                return func_recon("mat", body)
            return func_recon("mat", body, delim=f"\"{self.delim}\"")


class Binom(TypstObj):
    def __init__(
        self,
        upper: dict | TypstObj | List[dict | TypstObj],
        lower: dict | TypstObj | List[dict | TypstObj],
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "binom":
            raise ValueError("func must be binom")
        super().__init__(*args, **kwargs)
        self.func = "binom"
        self.upper = from_dict(upper) if isinstance(
            upper, dict) else [
                from_dict(e) if isinstance(e, dict) else e
                for e in upper
        ] if isinstance(upper, list) else upper
        self.lower = from_dict(lower) if isinstance(
            lower, dict) else [
                from_dict(e) if isinstance(e, dict) else e
                for e in lower
        ] if isinstance(lower, list) else lower

    def __eq__(self, value: Binom) -> bool:
        return isinstance(value, Binom) \
            and self.upper == value.upper \
            and self.lower == value.lower

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            upper = self.upper.reconstruct() if isinstance(
                self.upper, TypstObj
            ) else " ".join(
                [e.reconstruct() for e in self.upper])
            lower = self.lower.reconstruct() if isinstance(
                self.lower, TypstObj
            ) else "\\, ".join(
                [e.reconstruct() for e in self.lower])
            return func_recon(
                "binom",
                upper,
                lower
            )


class Root(TypstObj):
    def __init__(
        self,
        radicand: dict | TypstObj,
        index: Optional[dict | TypstObj] = None,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "root":
            raise ValueError("func must be root")
        super().__init__(*args, **kwargs)
        self.func = "root"
        self.radicand = from_dict(radicand) if isinstance(
            radicand, dict) else radicand
        self.index = from_dict(index) if isinstance(index, dict) else index

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            if self.index is not None:
                return func_recon(
                    "root",
                    self.index.reconstruct(),
                    self.radicand.reconstruct()
                )
            return func_recon("sqrt", self.radicand.reconstruct())


class H(TypstObj):
    def __init__(
        self,
        amount: str,
        weak: bool = True,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "h":
            raise ValueError("func must be h")
        super().__init__(*args, **kwargs)
        self.func = "h"
        self.amount = amount
        self.weak = weak

    def __eq__(self, value: H) -> bool:
        return isinstance(value, H) \
            and self.amount == value.amount \
            and self.weak == value.weak

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "#h",
                self.amount,
                weak=str(self.weak).lower()
            )


class Attach(TypstObj):
    def __init__(
        self,
        base: dict | TypstObj,
        t: Optional[dict | TypstObj] = None,
        b: Optional[dict | TypstObj] = None,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "attach":
            raise ValueError("func must be attach")
        super().__init__(*args, **kwargs)
        self.func = "attach"
        self.base = from_dict(base) if isinstance(
            base, dict) else base
        self.t = from_dict(t) if isinstance(
            t, dict) else t
        self.b = from_dict(b) if isinstance(
            b, dict) else b

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            res = self.base.reconstruct()
            if self.t is not None:
                res = f"{res} ^ ( {self.t.reconstruct()} )"
            if self.b is not None:
                res = f"{res} _ ( {self.b.reconstruct()} )"
            return res


class Op(TypstObj):
    def __init__(
        self,
        text: dict | TypstObj,
        limits: bool = False,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "op":
            raise ValueError("func must be op")
        super().__init__(*args, **kwargs)
        self.func = "op"
        self.text = from_dict(text) if isinstance(
            text, dict) else text
        self.limits = limits

    def __eq__(self, value: Op) -> bool:
        return isinstance(value, Op) \
            and self.text == value.text \
            and self.limits == value.limits

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "op",
                self.text.reconstruct(),
                limits=f"#{str(self.limits).lower()}"
            )


class Styled(TypstObj):
    def __init__(
        self,
        child: dict | TypstObj,
        styles: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "styled":
            raise ValueError("func must be styled")
        super().__init__(*args, **kwargs)
        self.func = "styled"
        self.child = from_dict(child) if isinstance(
            child, dict) else child
        self.styles = styles

    def __eq__(self, value: Styled) -> bool:
        return isinstance(value, Styled) \
            and self.child == value.child \
            and self.styles == value.styles

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return self.child.reconstruct()  # ! TO BE MODIFIED


class Move(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        dx: Optional[str] = None,
        dy: Optional[str] = None,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "move":
            raise ValueError("func must be move")
        super().__init__(*args, **kwargs)
        self.func = "move"
        self.dx = dx
        self.dy = dy
        self.body = from_dict(body) if isinstance(body, Dict) else body

    def __eq__(self, value: 'Move') -> bool:
        return isinstance(value, Move) \
            and self.dy == value.dy \
            and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "#move",
                self.body.reconstruct(),
                dx=self.dx,
                dy=self.dy
            )


class Strike(TypstObj):
    def __init__(
        self,
        offset: str,
        extent: str,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "strike":
            raise ValueError("func must be strike")
        super().__init__(*args, **kwargs)
        self.func = "strike"
        self.offset = offset
        self.extent = extent
        self.body = from_dict(body) if isinstance(body, Dict) else body

    def __eq__(self, value: 'Strike') -> bool:
        return isinstance(value, Strike) \
            and self.offset == value.offset \
            and self.extent == value.extent \
            and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "strike",
                self.body.reconstruct(),
                offset=self.offset,
                extent=self.extent
            )


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
