from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("align-point", pos=[])
class AlignPoint(TypstObj):

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return "&"