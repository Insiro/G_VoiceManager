from src.utils.error import ModManagerException
from .base import Cli, CONTINUE, BREAK


class GenerateCli(Cli):
    _level = "Main > Generate Mod"
    _menu = {
        0: "Cancel",
        1: "Select Mod Base (packed Mod or Original Source)",
        2: "Add Mod Source",
        3: "Clear Inputs",
        4: "Pack Mod file",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case 0:
                return BREAK
            case 1:
                self.__select_base()
                """TODO:Select Mod Base (packed Mod or Original Source)"""
            case 2:
                self.add_source_menu()
            case 3:
                self._service.clear_source()
            case 4:
                self.__pack_mod()
            case _:
                self.print_msg("wrong index selected")
        return CONTINUE

    def __select_base(self):
        mods = self._service.get_applied_mods()
        mods.append("original")
        mods.reverse()
        mod_name = self._sub_menu("Mod Base", "mod", mods)
        if mod_name is None:
            return
        if mod_name == "original":
            self._service.reset_base()
        else:
            self._service.select_base_mod()

    def add_source_menu(self):
        sources = self._service.get_mod_sources()
        source = self._sub_menu("Add Source", "mod source", sources)
        if source == None:
            return
        self._service.prepare_mod_source(source)

    def __pack_mod(self):
        while True:
            name = input("input new mod Name : ")
            try:
                self._service.pack_mod(name)
                self.print_msg("Successfully Packed mod", name)
            except ModManagerException as e:
                e.trace()
