from .. import TypstObj, func_recon
from ..typst_obj import typst_obj
from typing import Optional

@typst_obj("root", pos=["radicand"])
class Root(TypstObj):
    radicand: TypstObj
    index: Optional[dict | TypstObj] = None

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            if self.index is not None:
                return func_recon(
                    "root",
                    self.index.reconstruct(),
                    self.radicand.reconstruct()
                )
            return func_recon("sqrt", self.radicand.reconstruct())