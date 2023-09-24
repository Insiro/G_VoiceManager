from __future__ import annotations
import json
from os import path
from typing import Self


class ConfigData:
    temp_path: str
    resource_path: str
    # Path to Genshin Path, audio path will replaced as Symbolic Link
    genshin_path: str
    # path to Origianl Mod Source Files Saved
    mod_sources_path: str
    voice_lang: str
    backup_path: str
    locale: str
    hide: bool
    theme: str
    log: bool

    def __init__(self, data: ConfigData | None = None) -> None:
        if data is not None:
            self.copyData(data)

    @classmethod
    def fromData(cls, data: ConfigData) -> Self:
        return cls().copyData(data)

    @classmethod
    def new(
        cls,
        temp_path: str = ".\\temp",
        resource_path: str = ".\\resources",
        genshin_path: str = "C:\\Program Files\\Genshin Impact\\Genshin Impact game",
        mod_sources_path: str = ".\\resources\\mods",
        voice_lang: str = "Japanese",
        backup_path: str = ".\\resources\\backup",
        locale: str = "ko",
        hide: bool = False,
        theme="light_pink.xml",
        log=True,
        *args,
        **kwargs,
    ):
        ins = cls()
        ins.temp_path = temp_path
        ins.resource_path = resource_path
        ins.genshin_path = genshin_path
        ins.mod_sources_path = mod_sources_path
        ins.voice_lang = voice_lang
        ins.backup_path = backup_path
        ins.locale = locale
        ins.hide = hide
        ins.theme = theme
        ins.log = log
        return ins

    def copyData(self, data: ConfigData):
        self.temp_path = data.temp_path
        self.resource_path = data.resource_path
        self.genshin_path = data.genshin_path
        self.mod_sources_path = data.mod_sources_path
        self.voice_lang = data.voice_lang
        self.backup_path = data.backup_path
        self.locale = data.locale
        self.hide = data.hide
        self.theme = data.theme
        self.log = data.log
        return self

    def dict(self):
        return self.__dict__


assetSub = "GenshinImpact_Data\\StreamingAssets\\AudioAssets"


class Config(ConfigData):
    @property
    def wem_path(self) -> str:
        return path.join(self.temp_path, "wem")

    @property
    def output_pck_path(self) -> str:
        return path.join(self.temp_path, "output_pck")

    @property
    def packed_mods_path(self) -> str:  # Path to Mod Applied Path
        return path.join(self.resource_path, "applied")

    @property
    def lang_list_path(self) -> str:
        return path.join(self.genshin_path, assetSub)

    @property
    def sym_path(self) -> str:
        sym = path.join(self.genshin_path, assetSub, self.voice_lang)
        return sym

    @classmethod
    def load(cls, config_path: str | None = None):
        conf_path = "config.json" if config_path is None else config_path
        if path.isfile(conf_path):
            with open(conf_path, "r") as fp:
                conf = cls.new(**json.load(fp))
                conf._conf_path = conf_path
                return conf

        conf = cls.new()
        conf._conf_path = conf_path

        conf.save()
        return conf

    def save(self):
        with open(self._conf_path, "w") as fp:
            json.dump(ConfigData(self).__dict__, fp, indent=2)

    def dump(self) -> str:
        return json.dumps(ConfigData(self).__dict__, indent=2)
