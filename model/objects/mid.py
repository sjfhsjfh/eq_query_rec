from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("mid", pos=["body"])
class Mid(TypstObj):
    body: TypstObj
