from typing import TypedDict


class TabLocale(TypedDict):
    home: str
    gen_mod: str
    config: str


class ModsLocale(TypedDict):
    source_select: str
    mod_base: str
    input_mod_name: str
    gen_success: str
    pack_failed: str
    pack: str
    packing: str
    preparing: str


class MainLocale(TypedDict):
    restore: str
    select_mod: str
    backup_fail: str
    apply_mod: str
    link: str
    move: str
    backup: str


class Locale(TypedDict):
    tab: TabLocale
    mods: ModsLocale
    main: MainLocale
    apply: str
    refresh: str
    success: str
    failed: str
