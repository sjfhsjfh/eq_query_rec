from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("class", pos=["class_", "body"])
class Class(TypstObj):
    class_: str
    body: TypstObj

    def __init__(
        self,
        class_: str,
        body: TypstObj,
        *args, **kwargs
    ) -> None:
        if kwargs.get("func") != "class":
            raise ValueError("func must be class")
        super().__init__(*args, **kwargs)
        self.func = "class"
        self.class_ = kwargs.get("class")  # type: ignore
        if self.class_ is None:
            self.class_ = class_
        self.body = body

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            return func_recon(
                "class",
                f"\"{self.class_}\"",
                self.body.reconstruct()
            )
