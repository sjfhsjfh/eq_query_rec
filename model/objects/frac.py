from .. import TypstObj
from ..typst_obj import typst_obj


@typst_obj("frac", pos=["num", "denom"])
class Frac(TypstObj):
    num: TypstObj
    denom: TypstObj
    
    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return f"( {self.num.reconstruct()} )" \
                + " / " + f"( {self.denom.reconstruct()} )"
