from .base import Cli, BREAK, CONTINUE


class RestoreCli(Cli):
    _level = "Main > Restore"
    _menu = {
        0: "Cancel",
        1: "Symbolic Link",
        2: "Move Restore",
    }

    def _on_enter_menu(self) -> bool:
        if not self._service.validSymlink:
            self.print_msg(
                "there exist Directory, already restored or Backup is not applied"
            )
            return BREAK
        return CONTINUE

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case -1:
                exit()
            case 0:
                return BREAK
            case 1 | 2:
                self._service.restore(selected_idx == 1)
            case _:
                return CONTINUE
        return BREAK
