from .. import TypstObj, func_recon
from ..typst_obj import typst_obj

@typst_obj("op", pos=["text"])
class Op(TypstObj):
    text: dict | TypstObj
    limits: bool = False

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "op",
                self.text.reconstruct(),
                limits=f"#{str(self.limits).lower()}"
            )