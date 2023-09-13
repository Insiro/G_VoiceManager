import os
from os import path
from src.config import Config
from src.utils.dir import is_empty_dir

from src.utils.error import (
    ModNameNotValidException,
    ModSourceNotReadyException,
    NatValidDirException,
    NotValidSymLinkException,
)

from .mod_tool import ModTool


class ConfigService:
    def __init__(self, config: Config) -> None:
        self._conf = config
        self.reset()

        pass

    def reset(self):
        self.temp_path = self._conf.temp_path
        self.resource_path = self._conf.resource_path
        self.genshin_path = self._conf.genshin_path
        self.mod_sources_path = self._conf.mod_sources_path
        self.language = self._conf.language
        self.backup_path = self._conf.backup_path

    def commit(self):
        self._conf.temp_path = self.temp_path
        self._conf.resource_path = self.resource_path
        self._conf.genshin_path = self.genshin_path
        self._conf.mod_sources_path = self.mod_sources_path
        self._conf.language = self.language
        self._conf.backup_path = self.backup_path
        self._conf.save()

    def get_langList(self):
        return os.listdir(self._conf.lang_list_path)

    def format(self) -> str:
        conf = self._conf
        return "\n".join(
            [
                formatLine("genshin_path", conf.genshin_path, self.genshin_path),
                formatLine("backup_path", conf.backup_path, self.backup_path),
                formatLine(
                    "mod_sources_path", conf.mod_sources_path, self.mod_sources_path
                ),
                formatLine("resource_path", conf.resource_path, self.resource_path),
                formatLine("mod_language", conf.language, self.language),
                formatLine("temp_path", conf.temp_path, self.temp_path),
            ]
        )


def formatLine(name, conf, cur) -> str:
    return name + "\t:\t" + conf + "\t|\t" + cur


class ModService:
    _is_symlink_valid: bool

    def __init__(self, tool: ModTool) -> None:
        self._config = tool.config
        self._tool = tool
        self._selected_sources: list[str] = []
        self._configService = ConfigService(self._config)
        self.updateSymLinkState()

    # region property
    @property
    def validSymlink(self) -> bool:
        return self._is_symlink_valid

    @property
    def configservice(self):
        return self._configService

    @property
    def configString(self) -> str:
        return self._config.dump()

    # endregion

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

    def reset_base(self):
        self._tool.reset_input_path()

    # region Step 2 : mod source insert
    def select_base_mod(self, base_name: str):
        base_path = path.join(self._config.packed_mods_path, base_name)
        self.validDir(base_path)
        self._tool.set_input_path(base_path)
        pass

    def clear_source(self):
        try:
            self._tool.clear_mod_source()
            self._selected_sources.clear()
        except Exception as e:
            print(e)

    def prepare_mod_source(self, source_name: str):
        source_path = path.join(self._config.mod_sources_path, source_name)
        self.validDir(source_path)
        self._tool.prepare_mod_source(source_path)
        self._selected_sources.append(source_path)

    # endregion
    # Step 3 : generate mod files
    def pack_mod(self, mod_name: str):
        config = self._config
        if is_empty_dir(config.wem_path):
            raise ModSourceNotReadyException()
        mod_path = path.join(config.packed_mods_path, mod_name)
        self._tool.pack_mod_files(mod_path)

    # Step 4 : Apply Mod
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
