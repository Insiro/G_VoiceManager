from src.mod_tool import ModTool
from abc import ABCMeta, abstractmethod
from typing import Self

CONTINUE = True
BREAK = False


class Cli(metaclass=ABCMeta):
    _menu: dict[int, str] = {}
    _tool: ModTool

    @classmethod
    def run(cls, tool: ModTool):
        cli = cls()
        cli._tool = tool
        state = True
        while state:
            cli.__menu()
            selected = int(input("select menu : "))
            state = cli._action(selected)

    def __menu(self):
        print("menu\t|  Action")
        for key in self._menu:
            print(f"{key}\t:  {self._menu[key]}")

    @abstractmethod
    def _action(self, selected_idx: int) -> bool:
        if selected_idx == -1:
            exit()
        return BREAK


class MainCli(Cli):
    _menu = {
        -1: "Exit",
        0: "return",
        1: "Config",
        2: "BackUp mod",
        3: "Apply Mod",
        4: "Restore Mod",
        5: "Generate Mod",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case -1:
                exit()
            case 0:
                return False
            case 1:
                ConfigCli.run(self._tool)
            case 2:
                self._tool.move_and_link_original()
            case 3:
                mods = self._tool.get_applied_mods()
                while True:
                    print("0 : cancel")
                    for mod in mods:
                        print(mod)
                    mod_name = input("select mod name").strip()
                    if mod_name == "0":
                        break
                    elif mod_name == "-1":
                        exit()
                    if mod_name in mods:
                        self._tool.apply(mod_name)
                        break
            case 4:
                RestoreCli.run(self._tool)
            case 5:
                GenerateCli.run(self._tool)
        return CONTINUE


class RestoreCli(Cli):
    _menu = {
        -1: "Exit",
        0: "Cancel",
        1: "Symbolic Link",
        2: "Move Restore",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case -1:
                exit()
            case 0:
                return BREAK
            case 1:
                self._tool.restore(True)
            case 2:
                self._tool.restore(False)
            case _:
                return CONTINUE
        return BREAK


class GenerateCli(Cli):
    _menu = {
        -1: "Exit",
        0: "Cancel",
        1: "Select Mod Base (packed Mod or Original Source)",
        2: "Clear Inputs",
        3: "Add Mod Source",
    }

    def _action(self, selected_idx: int) -> bool:
        match selected_idx:
            case -1:
                exit()
            case 0:
                return BREAK
            case 1:
                """Select Mod Base (packed Mod or Original Source)"""
            case 2:
                self._tool.clear_mod_source()
            case 3:
                sources = self._tool.get_mod_sources()
                while True:
                    print("0 : cancel")
                    for source in sources:
                        print(source)
                    source = input("select mod source")
                    if source == "0":
                        break
                    elif source == "-1":
                        exit()
                    if source in sources:
                        self._tool.prepare_mod_source(source)
                        break
        return CONTINUE

    pass


class ConfigCli(Cli):
    pass
