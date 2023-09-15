from .abs_locale import Locale, MainLocale, ModsLocale


mod_locale = ModsLocale(
    select_mod_source="Select Mod Source",
    mod_base="Mod Base",
    input_mod_name="New Mod Name",
    generate_success="successfully Generated",
    pack_failed="Faild To Packing mod",
)

main_locale = MainLocale(
    restore="Restore",
    select_mod="--Select Mod--",
    backup_fail="Voice Not Installed or Already Backuped",
    apply_mod="Apply Mod",
)

locale_map = Locale(
    mods=mod_locale,
    main=main_locale,
    refresh="Refresh",
    apply="Apply",
    success="Success",
    failed="Failed",
)
