from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("limits", pos=["body"])
class Limits(TypstObj):
    body: TypstObj
