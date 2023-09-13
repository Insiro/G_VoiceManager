from .base import BREAK, CONTINUE, Cli


class ConfigCli(Cli):
    _level = "Main > Config"
    # TODO: impl Config Cli
    _menu = {0: "Cancel", 1: "Dump"}

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case 0:
                return BREAK
            case 1:
                self.print_msg(self._service.configString, False)
            case _:
                self.print_msg("wrong index selected")
        return CONTINUE
