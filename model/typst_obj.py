from typing import List

from . import TypstObj, func_recon


def typst_obj(name: str, pos: List[str]):
    """
    `pos` is to indicate the order of the positional arguments.
    """
    def decorator(cls):

        assert issubclass(cls, TypstObj)
        named = {
            k: cls.getattr(k)  # type: ignore
            for k, v in cls.__dict__.items()
            if not k.startswith("__") \
            and not callable(v)
        }
        """argname: default value"""
        defined_pos = set([
            k
            for k in cls.__annotations__
            if k not in named
        ])
        # All defined positional args(without default values)
        # should be in `pos`.
        assert set(pos) == defined_pos

        class __Wrapped(cls):

            def __init__(self, *args, **kwargs):
                if "func" in kwargs:
                    assert kwargs["func"] == name
                    del kwargs["func"]
                TypstObj.__init__(
                    self,
                    name,
                    *args,
                    **kwargs
                )
                setattr(self, "func", name)
                assert len(args) == len(pos)
                for an, av in zip(pos, args):
                    assert isinstance(
                        av,
                        cls.__annotations__.get(an)  # type: ignore
                    )
                    setattr(self, an, av)
                for k, v in kwargs.items():
                    setattr(self, k, v)

            def __ne__(self, value: object) -> bool:
                return not self == value

            def __eq__(self, other):
                if not isinstance(other, __class__):
                    return False
                for n in named:
                    if not getattr(self, n) == getattr(other, n):
                        return False
                for n in defined_pos:
                    if not getattr(self, n) == getattr(other, n):
                        return False
                return True

            def __repr__(self) -> str:
                return self.reconstruct()

            def __reconstruct(self) -> str:
                try:
                    return TypstObj.reconstruct(self)
                except:
                    try:
                        return super().reconstruct()
                    except:
                        return func_recon(
                            name,
                            *[
                                getattr(self, n)
                                for n in pos
                            ],
                            **{
                                k: getattr(self, k)
                                for k, v in named.items()
                                if getattr(self, k) != v
                            }
                        )

            def reconstruct(self) -> str:
                return self.__reconstruct()

        __Wrapped.__name__ = cls.__name__
        __Wrapped.__annotations__ = cls.__annotations__

        return __Wrapped
    return decorator
