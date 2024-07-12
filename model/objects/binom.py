from .. import TypstObj, func_recon
from ..typst_obj import typst_obj
from typing import List


@typst_obj("binom", pos=["upper", "lower"])
class Binom(TypstObj):
    upper: TypstObj | List[TypstObj]
    lower: TypstObj | List[TypstObj]
    
    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            upper = self.upper.reconstruct() if isinstance(
                self.upper, TypstObj
            ) else " ".join(
                [e.reconstruct() for e in self.upper])
            lower = self.lower.reconstruct() if isinstance(
                self.lower, TypstObj
            ) else "\\, ".join(
                [e.reconstruct() for e in self.lower])
            return func_recon(
                "binom",
                upper,
                lower
            )