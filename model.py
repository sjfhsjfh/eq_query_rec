from __future__ import annotations
from typing import Dict, List, Optional


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
    arg_items = list(map(lambda x: f"{x[0]}: {str(x[1])}", kwargs.items()))
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

    def __str__(self) -> str:
        return self.reconstruct()

    def __repr__(self) -> str:
        res = self.__dict__
        PROTECTED = []
        for p in PROTECTED:
            res.pop(p)
        s = f"{self.func}({', '.join([f'{k}: {v}' for k, v in res.items()])})"
        return s

    def reconstruct(self) -> str:
        for k, v in CONSTS.items():
            if v.__eq__(self):
                return f"{k}"
        raise NotImplementedError


class Equation(TypstObj):

    def __init__(
        self,
        block: bool,
        body: dict | TypstObj,
        numbering: Optional[str] = None,
        supplement: Optional[dict | TypstObj] = None,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "equation":
            raise ValueError("func must be equation")
        super().__init__(*args, **kwargs)
        self.func = "equation"
        self.block = block
        self.numbering = numbering
        self.number_align = kwargs.get("number-align")
        self.body = from_dict(body) if isinstance(body, dict) else body
        self.supplement = from_dict(supplement) if isinstance(
            supplement, dict) else supplement

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            res = self.body.reconstruct()
            if self.block:
                res = f" {res} "
            res = f"${res}$"

            # Remove consecutive spaces
            import re

            parts = re.split(r'((?<!\\)".*?(?<!\\)")', res)
            parts = [re.sub(r'\s+', ' ', part)
                     if not part.startswith('"') else part for part in parts]
            res = "".join(parts)

            return res


class Overline(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "overline":
            raise ValueError("func must be overline")
        super().__init__(*args, **kwargs)
        self.func = "overline"
        self.body = from_dict(body) if isinstance(body, dict) else body

    def __eq__(self, value: Overline) -> bool:
        return isinstance(value, Overline) and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("overline", self.body.reconstruct())


class Underline(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "underline":
            raise ValueError("func must be underline")
        super().__init__(*args, **kwargs)
        self.func = "underline"
        self.body = from_dict(body) if isinstance(body, dict) else body

    def __eq__(self, value: Underline) -> bool:
        return isinstance(value, Underline) and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("underline", self.body.reconstruct())


class Mid(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "mid":
            raise ValueError("func must be mid")
        super().__init__(*args, **kwargs)
        self.func = "mid"
        self.body = from_dict(body) if isinstance(body, dict) else body

    def __eq__(self, value: Mid) -> bool:
        return isinstance(value, Mid) and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("mid", self.body.reconstruct())


class Limits(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "limits":
            raise ValueError("func must be limits")
        super().__init__(*args, **kwargs)
        self.func = "limits"
        self.body = from_dict(body) if isinstance(body, dict) else body

    def __eq__(self, value: Limits) -> bool:
        return isinstance(value, Limits) and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("limits", self.body.reconstruct())


class Cancel(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        angle: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "cancel":
            raise ValueError("func must be cancel")
        super().__init__(*args, **kwargs)
        self.func = "cancel"
        self.body = from_dict(body) if isinstance(body, dict) else body
        self.angle = angle

    def __eq__(self, value: Cancel) -> bool:
        return isinstance(value, Cancel) \
            and self.body == value.body \
            and self.angle == value.angle

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "cancel",
                self.body.reconstruct(),
                angle=self.angle
            )


class Accent(TypstObj):
    def __init__(
        self,
        base: dict | TypstObj,
        accent: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "accent":
            raise ValueError("func must be accent")
        super().__init__(*args, **kwargs)
        self.func = "accent"
        self.base = from_dict(base) if isinstance(base, dict) else base
        self.accent = accent

    def __eq__(self, value: Accent) -> bool:
        return isinstance(value, Accent) \
            and self.base == value.base \
            and self.accent == value.accent

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            global ACCENTS
            if ACCENTS[self.accent]["callable"]:
                return func_recon(ACCENTS[self.accent]["name"], self.base.reconstruct())
            else:
                return func_recon("accent", self.base.reconstruct(), ACCENTS[self.accent]["shortcut"])

class Class(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        # class: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "class":
            raise ValueError("func must be class")
        super().__init__(*args, **kwargs)
        self.func = "class"
        self.body = from_dict(body) if isinstance(body, dict) else body
        self.class_ = kwargs.get("class")

    def __eq__(self, value: Class) -> bool:
        return isinstance(value, Class) \
            and self.body == value.body \
            and self.class_ == value.class_

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("class", f"\"self.class_\"", self.body.reconstruct())


class Text(TypstObj):
    def __init__(
        self,
        text: str,
        func: str = "text",
        *args, **kwargs
    ) -> None:
        if func != "text":
            raise ValueError("func must be text")
        super().__init__(func=func, *args, **kwargs)
        self.func = "text"
        self.text = text

    def __eq__(self, value: Text) -> bool:
        return isinstance(value, Text) and self.text == value.text

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            if len(self.text) == 1:
                return escape(self.text)

            def str_escape(c): return escape(c, chars='\\"')
            return f"""\"{''.join(map(str_escape, self.text))}\""""


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


class Cases(TypstObj):
    def __init__(
        self,
        children: list[dict | TypstObj],
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "cases":
            raise ValueError("func must be cases")
        super().__init__(*args, **kwargs)
        self.func = "cases"
        self.children = [from_dict(child) if isinstance(
            child, dict) else child for child in children]

    def __eq__(self, value: Cases) -> bool:
        if not isinstance(value, Cases):
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
            return func_recon(
                "cases",
                *[child.reconstruct() for child in self.children]
            )


class Vec(TypstObj):
    def __init__(
        self,
        children: list[dict | TypstObj],
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "vec":
            raise ValueError("func must be vec")
        super().__init__(*args, **kwargs)
        self.func = "vec"
        self.children = [from_dict(child) if isinstance(
            child, dict) else child for child in children]

    def __eq__(self, value: Vec) -> bool:
        if not isinstance(value, Vec):
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
            return func_recon(
                "vec",
                *[child.reconstruct() for child in self.children]
            )


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
            return func_recon("mat", body, delim=f"\"self.delim\"")


class LR(TypstObj):
    def __init__(
        self,
        body: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "lr":
            raise ValueError("func must be lr")
        super().__init__(*args, **kwargs)
        self.func = "lr"
        self.body = from_dict(body) if isinstance(body, dict) else body

    def __eq__(self, value: LR) -> bool:
        return isinstance(value, LR) and self.body == value.body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            if isinstance(self.body, Sequence):
                c = self.body.children
                if len(c) >= 2:
                    if c[0] == Text("(") and c[-1] == Text(")"):
                        return self.body.reconstruct()
                    if c[0] == Text("[") and c[-1] == Text("]"):
                        return self.body.reconstruct()
                    if c[0] == Text("{") and c[-1] == Text("}"):
                        return self.body.reconstruct()
            return func_recon("lr", self.body.reconstruct())


class Space(TypstObj):
    def __init__(
        self,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "space":
            raise ValueError("func must be space")
        super().__init__(*args, **kwargs)
        self.func = "lr"

    def __eq__(self, value: Space) -> bool:
        return isinstance(value, Space)

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            # return "med"
            return " "  # ! TO BE MODIFIED


class Primes(TypstObj):
    def __init__(
        self,
        count: int,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "primes":
            raise ValueError("func must be primes")
        super().__init__(*args, **kwargs)
        self.func = "primes"
        self.count = count

    def __eq__(self, value: Primes) -> bool:
        return isinstance(value, Primes) and self.count == value.count

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("primes", f"#{self.count}")


class LineBreak(TypstObj):
    def __init__(
        self,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "linebreak":
            raise ValueError("func must be linebreak")
        super().__init__(*args, **kwargs)
        self.func = "linebreak"

    def __eq__(self, value: LineBreak) -> bool:
        return isinstance(value, LineBreak)

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return r"\ "


class AlignPoint(TypstObj):
    def __init__(
        self,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "align-point":
            raise ValueError("func must be align-point")
        super().__init__(*args, **kwargs)
        self.func = "align-point"

    def __eq__(self, value: AlignPoint) -> bool:
        return isinstance(value, AlignPoint)

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return "&"


class Frac(TypstObj):
    def __init__(
        self,
        num: dict | TypstObj,
        denom: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "frac":
            raise ValueError("func must be frac")
        super().__init__(*args, **kwargs)
        self.func = "frac"
        self.num = from_dict(num) if isinstance(
            num, dict) else num
        self.denom = from_dict(denom) if isinstance(
            denom, dict) else denom

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return f"( {self.num.reconstruct()} )" \
                + " / " + f"( {self.denom.reconstruct()} )"


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
    if d["func"] == "mid":
        return Mid(**d)
    if d["func"] == "limits":
        return Limits(**d)
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


load_consts()
