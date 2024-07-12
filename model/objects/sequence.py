from .. import TypstObj, func_recon, CONST_KMP, CONSTS
from ..typst_obj import typst_obj
from typing import List


@typst_obj("sequence", pos=["children"])
class Sequence(TypstObj):
    children: list[dict | TypstObj]

    def reconstruct(self) -> str:
        try:
            return super().reconstruct()
        except:
            def process_slice(s: List[TypstObj]):
                # KMP find Sequence in CONSTS
                for k, v in CONSTS.items():
                    if not isinstance(v, Sequence):
                        continue
                    i = 0
                    j = 0
                    while i < len(s) and j < len(v.children):
                        if s[i] == v.children[j]:
                            i += 1
                            j += 1
                            if j == len(v.children):
                                return process_slice(s[:i - j]) \
                                    + [k] + process_slice(s[i:])
                        else:
                            t = CONST_KMP[k]
                            if j == 0:
                                i += 1
                            else:
                                j = t[j - 1]
                return [c.reconstruct() for c in s]

            return " ".join(process_slice(self.children))