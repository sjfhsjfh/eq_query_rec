from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("overbrace", pos=["body"])
class Overbrace(TypstObj):
    body: TypstObj
