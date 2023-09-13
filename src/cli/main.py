from src.utils.error import NotValidDirException
from . import *


class MainCli(Cli):
    _level = "Main"
    _menu = {
        0: "Cancel",
        1: "Config",
        2: "BackUp Original Resource",
        3: "Apply Mod",
        4: "Restore Mod",
        5: "Generate Mod",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case 0:
                return False
            case 1:
                ConfigCli.run(self._service)
            case 2:
                self.__backup()
            case 3:
                self.__apply_menu()
            case 4:
                RestoreCli.run(self._service)
            case 5:
                GenerateCli.run(self._service)
            # case _:
            # self.print_msg("wrong index selected")
        return CONTINUE

    def __backup(self):
        try:
            self._service.isolate_original()
            self.print_msg("backup complete")
        except NotValidDirException as e:
            e.trace_back()
            self.print_msg("Error : already symbloc link is generated")

    def __apply_menu(self):
        mods = self._service.get_applied_mods()
        mod_name = self._sub_menu("Apply Mod", "mod", mods)
        if mod_name == None:
            return
        self._service.apply(mod_name)
        self.print_msg(f"mod {mod_name} applied")
