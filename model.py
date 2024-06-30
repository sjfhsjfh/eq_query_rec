from __future__ import annotations


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
        print(f"Current type {self.func}")
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
        self.block = block
        self.numbering = numbering
        self.number_align = kwargs.get("number-align")
        self.body = from_dict(body) if isinstance(body, dict) else body
        self.supplement = from_dict(supplement) if isinstance(
            supplement, dict) else supplement

    def reconstruct(self) -> str:
        res = self.body.reconstruct()
        if self.block:
            res = f" {res} "
        return f"${res}$"


class Text(TypstObj):
    def __init__(
        self,
        text: str,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "text":
            raise ValueError("func must be text")
        super().__init__(*args, **kwargs)
        self.text = text


class Sequence(TypstObj):

    def __init__(
        self,
        children: list[dict | TypstObj],
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "sequence":
            raise ValueError("func must be sequence")
        super().__init__(*args, **kwargs)
        self.children = [from_dict(child) if isinstance(
            child, dict) else child for child in children]

    def reconstruct(self) -> str:
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
        self.body = from_dict(body) if isinstance(body, dict) else body


class Space(TypstObj):
    def __init__(
        self,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "space":
            raise ValueError("func must be space")
        super().__init__(*args, **kwargs)

    def reconstruct(self) -> str:
        return "med"


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
        self.num = from_dict(num) if isinstance(
            num, dict) else num
        self.denom = from_dict(denom) if isinstance(
            denom, dict) else denom


class Root(TypstObj):
    def __init__(
        self,
        radicand: dict | TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "root":
            raise ValueError("func must be root")
        super().__init__(*args, **kwargs)
        self.radicand = from_dict(radicand) if isinstance(
            radicand, dict) else radicand


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
    raise ValueError(f"Invalid TypstObj {d['func']}")
