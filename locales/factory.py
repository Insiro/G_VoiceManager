def locale(locale: str):
    match locale[:2]:
        case "ko":
            from .ko import locale_map
        case _:
            from .en import locale_map

    return locale_map
