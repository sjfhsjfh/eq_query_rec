from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("cases", pos=["children"])
class Cases(TypstObj):
    children: list[TypstObj]

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "cases",
                *[child.reconstruct() for child in self.children]
            )