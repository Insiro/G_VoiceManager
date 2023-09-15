def locale(locale: str):
    match locale:
        case "en":
            from .en import locale_map
        case _:
            from .en import locale_map

    return locale_map
