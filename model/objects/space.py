from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("space", pos=[])
class Space(TypstObj):

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            # return "med"
            return " "  # ! TO BE MODIFIED