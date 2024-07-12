from .. import TypstObj, func_recon
from ..typst_obj import typst_obj
from typing import Optional

@typst_obj("attach", pos=["base"])
class Attach(TypstObj):
    base: dict | TypstObj
    t: Optional[dict | TypstObj] = None
    b: Optional[dict | TypstObj] = None

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            res = self.base.reconstruct()
            if self.b is not None:
                res = f"{res} _ ( {self.b.reconstruct()} )"
            if self.t is not None:
                res = f"{res} ^ ( {self.t.reconstruct()} )"

            return res