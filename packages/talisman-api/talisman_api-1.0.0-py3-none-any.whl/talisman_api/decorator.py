from .abstract import AbstractTalismanAPI


def version(v: str):
    def decorate(cls: type[AbstractTalismanAPI]):
        cls._VERSION = v
        return cls

    return decorate
