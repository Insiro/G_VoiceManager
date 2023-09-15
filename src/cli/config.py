from .base import BREAK, CONTINUE, Cli
from os import path


class ConfigCli(Cli):
    _level = "Main > Config"
    _menu = {
        0: "Cancel",
        1: "Change Temp Path",
        2: "Change Resource Path",
        3: "Change Mod Source Path",
        4: "Change Genshin Path",
        5: "Change Original Source Backup Path",
        6: "Change Mod Language",
        7: "Commit Setting",
    }

    def _action(self, selected_idx: int) -> bool:
        if selected_idx == 0:
            return BREAK
        if selected_idx > 7 or selected_idx < 0:
            return CONTINUE
        if selected_idx == 7:
            self.conf_service.commit()
        if selected_idx == 6:
            selected = self._sub_menu(
                "Language", "voice language", self.conf_service.voice_list
            )
            if selected == None:
                return CONTINUE
            self.conf_service.voice_lang = selected
            return CONTINUE

        if selected_idx == 5:
            print("recommand to select save disk drive with genshin")
        selected = self.select_path(selected_idx)
        if selected == None:
            return CONTINUE
        match selected_idx:
            case 1:
                self.conf_service.temp_path = selected
            case 2:
                self.conf_service.resource_path = selected
            case 3:
                self.conf_service.mod_sources_path = selected
            case 4:
                self.conf_service.genshin_path = selected
            case 5:
                self.conf_service.backup_path = selected
        return CONTINUE

    def select_path(self, menu_idx: int) -> str | None:
        while True:
            print(f"change {self._menu[menu_idx][6:]}")
            spath = input(f"enter path : ").strip()
            if not path.isdir(spath):
                self.print_msg("wrong path selected")
                return None
            return spath

    def _on_enter_menu(self) -> bool:
        self.conf_service = self._bin.conf_service
        print(self.conf_service.format())
        return True
