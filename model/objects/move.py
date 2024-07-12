from .. import TypstObj, func_recon
from ..typst_obj import typst_obj
from typing import Optional

@typst_obj("move", pos=["body"])
class Move(TypstObj):
    body: dict | TypstObj
    dx: Optional[str] = None
    dy: Optional[str] = None

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "#move",
                self.body.reconstruct(),
                dx=self.dx,
                dy=self.dy
            )