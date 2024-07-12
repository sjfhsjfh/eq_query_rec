from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("strike", pos=["offset", "extent", "body"])
class Strike(TypstObj):
    offset: str
    extent: str
    body: dict | TypstObj

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "strike",
                self.body.reconstruct(),
                offset=self.offset,
                extent=self.extent
            )