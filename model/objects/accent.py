from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("accent", pos=["base", "accent"])
class Accent(TypstObj):
    base: TypstObj
    accent: str
