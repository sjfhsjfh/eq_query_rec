from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("linebreak", pos=[])
class LineBreak(TypstObj):

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return r"\ "