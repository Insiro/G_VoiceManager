import os
from os import path

from src.utils.dir import is_empty_dir
from src.utils.error import *

from .config import Config, ConfigData
from .mod_tool import ModTool


class ConfigService(ConfigData):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._conf = config
        self.reset()

        pass

    def reset(self):
        self.temp_path = self._conf.temp_path
        self.resource_path = self._conf.resource_path
        self.genshin_path = self._conf.genshin_path
        self.mod_sources_path = self._conf.mod_sources_path
        self.voice_lang = self._conf.voice_lang
        self.backup_path = self._conf.backup_path
        self.locale = self._conf.locale

    def commit(self):
        self._conf.temp_path = self.temp_path
        self._conf.resource_path = self.resource_path
        self._conf.genshin_path = self.genshin_path
        self._conf.mod_sources_path = self.mod_sources_path
        self._conf.voice_lang = self.voice_lang
        self._conf.backup_path = self.backup_path
        self._conf.locale = self.locale
        self._conf.save()

    @property
    def voice_list(self):
        items = os.listdir(self._conf.lang_list_path)
        langs = []
        for item in items:
            item_dir = path.join(self._conf.lang_list_path, item)
            if path.isfile(item_dir):
                continue
            langs.append(item)

        return langs

    def format(self) -> str:
        conf = self._conf
        plen = max(
            len(conf.genshin_path),
            len(conf.backup_path),
            len(conf.mod_sources_path),
            len(conf.resource_path),
            len(conf.temp_path),
        )

        return "\n".join(
            [
                formatLine("genshin_path", conf.genshin_path, self.genshin_path, plen),
                formatLine("backup_path", conf.backup_path, self.backup_path, plen),
                formatLine(
                    "mod_sources_path",
                    conf.mod_sources_path,
                    self.mod_sources_path,
                    plen,
                ),
                formatLine(
                    "resource_path", conf.resource_path, self.resource_path, plen
                ),
                formatLine("mod_language", conf.voice_lang, self.voice_lang, plen),
                formatLine("temp_path", conf.temp_path, self.temp_path, plen),
                formatLine("display language", conf.locale, self.locale, plen),
            ]
        )


def formatLine(name, conf, cur, confLen: int) -> str:
    return f"{name:<20} : {conf:<{confLen+1}} | {cur}"


class ModService:
    _is_symlink_valid: bool

    def __init__(self, tool: ModTool) -> None:
        self._config = tool.config
        self._tool = tool
        self._selected_sources: list[str] = []
        self.updateSymLinkState()

    # region property
    @property
    def validSymlink(self) -> bool:
        return self._is_symlink_valid

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
            raise NotValidDirException()
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
        if not self.validSymlink and path.exists(self._config.sym_path):
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
            raise NotValidDirException()

    def updateSymLinkState(self):
        self._is_symlink_valid = path.islink(self._config.sym_path)
