from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("underline", pos=["body"])
class Underline(TypstObj):
    body: TypstObj
