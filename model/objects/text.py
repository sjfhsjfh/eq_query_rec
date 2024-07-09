from .. import escape, TypstObj
from ..typst_obj import typst_obj


@typst_obj("text", pos=["text"])
class Text(TypstObj):
    text: str

    def reconstruct(self, chars="\\,;.$&#\"'") -> str:
        return escape(self.text, chars=chars)
