from src.mod_tool import ModTool
from abc import ABCMeta, abstractmethod
from src.service import DirService
from time import sleep
import os

CONTINUE = True
BREAK = False


class Cli(metaclass=ABCMeta):
    _menu: dict[int, str] = {}
    _tool: ModTool
    _service: DirService
    _level: str = "Menu Name, Required Override"

    @classmethod
    def run(cls, service: DirService):
        cli = cls()
        cli._service = service
        state = True
        while state:
            if not cli._on_enter_menu():
                break
            cli.__menu()
            selected = cli.__get_input_number("menu")
            match selected:
                case None:
                    cli.print_msg("wrong index selected")
                case -1:
                    exit()
                case _:
                    state = cli._action(selected)

    def _on_enter_menu(self) -> bool:
        return True

    def __menu(self):
        print("\n==========================")
        print(f"menu\t|  {self._level}")
        for key in self._menu:
            print(f"{key}\t:  {self._menu[key]}")
        print("==========================")

    @abstractmethod
    def _action(self, selected_idx: int) -> bool:
        if selected_idx == -1:
            exit()
        return BREAK

    def clear_terminal(self):
        os.system("cls||clear")

    def print_msg(self, msg: str, clear=True):
        print(msg)
        sleep(1)
        if clear:
            self.clear_terminal()

    def __get_input_number(self, msg: str) -> int | None:
        selected = input(f"select {msg} number : ")
        if selected == "-1":
            return -1
        if selected.isdecimal():
            return int(selected)
        return None

    def _sub_menu(
        self, mod_name: str, selection_name: str, options: list[str]
    ) -> str | None:
        while True:
            self.clear_terminal()
            print("\n==========================")
            print(f"menu\t| {self._level} > {mod_name}")
            print("0\t: cancel")
            for idx, option in enumerate(options):
                print(f"{idx+1}\t: {option}")
            print("\n==========================")

            selected = self.__get_input_number(selection_name)
            if selected is not None:
                if selected == 0:
                    return None
                if selected - 1 < len(options):
                    return options[selected - 1]
            self.print_msg("wrong index selected")
