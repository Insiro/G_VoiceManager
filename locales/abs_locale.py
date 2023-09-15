from typing import TypedDict


class ModsLocale(TypedDict):
    select_mod_source: str
    mod_base: str
    input_mod_name: str
    generate_success: str
    pack_failed: str


class MainLocale(TypedDict):
    restore: str
    select_mod: str
    backup_fail: str
    apply_mod:str


class Locale(TypedDict):
    mods: ModsLocale
    main: MainLocale
    apply: str
    refresh: str
    success: str
    failed: str
