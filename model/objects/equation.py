from typing import Optional
from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("equation", pos=["body", "block"])
class Equation(TypstObj):
    block: bool
    body: TypstObj
    numbering: Optional[str] = None
    number_align: Optional[str] = None
    supplement: Optional[TypstObj] = None

    def __init__(
        self,
        block: bool,
        body: TypstObj,
        numbering: Optional[str] = None,
        supplement: Optional[TypstObj] = None,
        *args, **kwargs
    ) -> None:
        if "func" in kwargs:
            assert kwargs["func"] == "equation"
            del kwargs["func"]
        TypstObj.__init__(
            self,
            "equation",
            *args,
            **kwargs
        )
        setattr(self, "func", "equation")
        pos = ["body", "block"]
        assert len(args) == len(pos)
        for an, av in zip(pos, args):
            assert isinstance(
                av,
                __class__.__annotations__.get(an)  # type: ignore
            )
            setattr(self, an, av)
        for k, v in kwargs.items():
            setattr(self, k, v)

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
