from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("h", pos=["amount"])
class H(TypstObj):
    amount: str
    weak: bool = True

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "#h",
                self.amount,
                weak=str(self.weak).lower()
            )