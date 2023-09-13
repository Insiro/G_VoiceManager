import os
from os import path

from src.utils.error import (
    ModNameNotValidException,
    NatValidDirException,
    NotValidSymLinkException,
)

from .mod_tool import ModTool


class Bin:
    pass


class configService:
    pass


class DirService:
    _is_symlink_valid: bool

    def __init__(self, tool: ModTool) -> None:
        self._config = tool.config
        self._tool = tool
        self._selected_sources: list[str] = []
        self.updateSymLinkState()

    @property
    def validSymlink(self) -> bool:
        return self._is_symlink_valid

    @property
    def configString(self) -> str:
        return self._config.dump()

    def get_applied_mods(self) -> list[str]:
        items = os.listdir(self._config.packed_mods_path)
        return [
            item
            for item in items
            if path.isdir(path.join(self._config.packed_mods_path, item))
        ]

    def get_mod_sources(self) -> list[str]:
        items = os.listdir(self._config.mod_sources_path)
        return [
            item
            for item in items
            if path.isdir(path.join(self._config.mod_sources_path, item))
        ]

    # Step 1 : Backup
    def isolate_original(self):
        if self._is_symlink_valid:
            raise NatValidDirException()
        self._tool.move_and_link_original()
        self._is_symlink_valid = True

    # region Step 2 : mod source insert
    def select_base_mod(self, base: str):
        # TODO: select base mod
        self.validDir(base)
        self._tool.set_input_path(base)
        pass

    def clear_source(self):
        try:
            self._tool.clear_mod_source()
            self._selected_sources.clear()
        except:
            pass

    def prepare_mod_source(self, source_name: str):
        source_path = path.join(self._config.mod_sources_path, source_name)
        self.validDir(source_path)
        self._tool.prepare_mod_source(source_path)
        self._selected_sources.append(source_path)

    # endregion
    def apply(self, mod_name):
        print(self._config.sym_path)
        if not self.validSymlink:
            raise NotValidSymLinkException()
        mod_path = path.join(self._config.packed_mods_path, mod_name)
        if not path.isdir(mod_path):
            raise ModNameNotValidException()
        self._tool.apply(mod_path)

    def restore(self, link=True):
        if not self.validSymlink:
            raise NotValidSymLinkException()
        self._tool.restore(link)

    def validDir(self, dir: str):
        if not path.isdir(dir):
            raise NatValidDirException()

    def updateSymLinkState(self):
        self._is_symlink_valid = path.islink(self._config.sym_path)
