from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("overbracket", pos=["body"])
class Overbracket(TypstObj):
    body: TypstObj
