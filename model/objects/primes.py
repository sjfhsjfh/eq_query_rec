from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("primes", pos=["count"])
class Primes(TypstObj):
    count: int

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon("primes", f"#{self.count}")