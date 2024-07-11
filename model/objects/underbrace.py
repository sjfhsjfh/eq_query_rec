from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("underbrace", pos=["body"])
class Underbrace(TypstObj):
    body: TypstObj
