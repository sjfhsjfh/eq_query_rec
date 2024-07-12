from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("vec", pos=["children"])
class Vec(TypstObj):
    children: list[TypstObj]

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "vec",
                *[child.reconstruct() for child in self.children]
            )