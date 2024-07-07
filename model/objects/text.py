from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("text", pos=["text"])
class Text(TypstObj):
    text: str

    def reconstruct(self) -> str:
        return self.text
