from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("scripts", pos=["body"])
class Scripts(TypstObj):
    body: TypstObj
