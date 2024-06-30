from __future__ import annotations
from typing import Optional


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

    def __repr__(self) -> str:
        return self.reconstruct()

    def reconstruct(self) -> str:
        for k, v in CONSTS.items():
            if v.__eq__(self):
                return f"{k}"
        # print(f"Current type {self.func}")
        raise NotImplementedError


class Equation(TypstObj):

    def __init__(
        self,
        block: bool,
        numbering: str,
        body: dict | TypstObj,
        supplement: dict | TypstObj,
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


class Text(TypstObj):
    def __init__(
        self,
        text: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "text":
            raise ValueError("func must be text")
        super().__init__(*args, **kwargs)
        self.func = "text"
        self.text = text

    def __eq__(self, value: Text) -> bool:
        return isinstance(value, Text) and self.text == value.text

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return self.text


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
            return " ".join([child.reconstruct() for child in self.children])


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

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return f"lr({self.body.reconstruct()})"


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
            return ""  # ! TO BE MODIFIED


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
            return f"({self.num.reconstruct()}) / ({self.denom.reconstruct()})"


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
                return f"root({self.index.reconstruct()}," + \
                    f"{self.radicand.reconstruct()})"
            return f"sqrt({self.radicand.reconstruct()})"


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
            return ""  # ! TO BE MODIFIED


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
                res = f"{res}^({self.t.reconstruct()})"
            if self.b is not None:
                res = f"{res}_({self.b.reconstruct()})"
            return res


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
            return ""  # ! TO BE MODIFIED


def from_dict(d: dict) -> TypstObj:
    if d["func"] == "equation":
        return Equation(**d)
    if d["func"] == "sequence":
        return Sequence(**d)
    if d["func"] == "text":
        return Text(**d)
    if d["func"] == "lr":
        return LR(**d)
    if d["func"] == "space":
        return Space(**d)
    if d["func"] == "frac":
        return Frac(**d)
    if d["func"] == "root":
        return Root(**d)
    if d["func"] == "attach":
        return Attach(**d)
    if d["func"] == "h":
        return H(**d)
    if d["func"] == "styled":
        return Styled(**d)
    raise ValueError(f"Invalid TypstObj {d['func']}")


CONSTS = {}


def load_consts(fp="const.json"):
    global CONSTS
    from pathlib import Path
    import json

    DIR = Path(__file__).parent
    with open(DIR / fp, "r") as f:
        CONSTS.update({k: from_dict(v) for k, v in json.load(f).items()})


load_consts()
