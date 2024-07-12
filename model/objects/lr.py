from .. import TypstObj, func_recon
from .text import Text
from .space import Space
from .sequence import Sequence

from ..typst_obj import typst_obj


@typst_obj("lr", pos=["body"])
class LR(TypstObj):
    body: TypstObj

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            if isinstance(self.body, Sequence):
                c = self.body.children
                first_index = next(
                    (
                        index
                        for index, item in enumerate(c)
                        if not isinstance(item, Space)
                    ),
                    None,
                )
                last_index = next(
                    (
                        len(c) - 1 - index
                        for index, item in enumerate(reversed(c))
                        if not isinstance(item, Space)
                    ),
                    None,
                )
                c = c[first_index: last_index + 1]

                if len(c) >= 2:
                    if c[0] == Text("(") and c[-1] == Text(")"):
                        return self.body.reconstruct()
                    if c[0] == Text("[") and c[-1] == Text("]"):
                        return self.body.reconstruct()
                    if c[0] == Text("{") and c[-1] == Text("}"):
                        return self.body.reconstruct()
            return func_recon("lr", self.body.reconstruct())