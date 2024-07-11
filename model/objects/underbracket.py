from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("underbracket", pos=["body"])
class Underbracket(TypstObj):
    body: TypstObj
