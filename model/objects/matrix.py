from .. import TypstObj, func_recon
from ..typst_obj import typst_obj


@typst_obj("matrix", pos=["rows"])
class Matrix(TypstObj):
    rows: list[list[dict | TypstObj]]
    delim: str = "("

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            rows = []
            for row in self.rows:
                rows.append(", ".join([cell.reconstruct() for cell in row]))
            body = '; '.join(rows)
            if self.delim == "(" or self.delim is None:
                return func_recon("mat", body)
            return func_recon("mat", body, delim=f"\"{self.delim}\"")