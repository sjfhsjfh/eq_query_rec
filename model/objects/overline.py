from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("overline", pos=["body"])
class Overline(TypstObj):
    body: TypstObj
