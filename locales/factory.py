from enum import Enum


class Lang(Enum):
    en = "English"
    ko = "한국어"

    @classmethod
    def fromStr(cls, txt):
        match txt:
            case "ko" | "한국어":
                return Lang.ko
            case _:
                return Lang.en


def locale(locale: str):
    match Lang.fromStr(locale):
        case Lang.ko:
            from .ko import locale_map
        case _:
            from .en import locale_map

    return locale_map
