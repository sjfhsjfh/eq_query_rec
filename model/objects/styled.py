from .. import TypstObj, func_recon
from ..typst_obj import typst_obj

@typst_obj("styled", pos=["child", "styles"])
class Styled(TypstObj):
    child: dict | TypstObj
    styles: str

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return self.child.reconstruct()  # ! TO BE MODIFIED