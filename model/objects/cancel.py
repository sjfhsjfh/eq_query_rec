from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("cancel", pos=["body"])
class Cancel(TypstObj):
    body: str
    angle: str = ""  # ! To be modified
