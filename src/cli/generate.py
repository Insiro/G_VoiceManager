from .base import Cli, CONTINUE, BREAK


class GenerateCli(Cli):
    _level = "Main > Restore"
    _menu = {
        0: "Cancel",
        1: "Select Mod Base (packed Mod or Original Source)",
        2: "Clear Inputs",
        3: "Add Mod Source",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case 0:
                return BREAK
            case 1:
                """Select Mod Base (packed Mod or Original Source)"""
            case 2:
                self._service.clear_source()
            case 3:
                self.add_source_menu()
            case _:
                self.print_msg("wrong index selected")
        return CONTINUE

    def add_source_menu(self):
        sources = self._service.get_mod_sources()
        source = self._sub_menu("Add Source", "mod source", sources)
        if source == None:
            return
        self._service.prepare_mod_source(source)
