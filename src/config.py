from os import path
import json


class Config:
    temp_path: str
    resource_path: str
    genshin_path: str  # Path to Genshin Path, audio path will replaced as Symbolic Link
    mod_sources_path: str  # path to Origianl Mod Source Files Saved
    language: str
    backup_path: str

    @staticmethod
    def __assign(
        temp_path: str,
        resource_path: str,
        genshin_path: str,
        mod_sources_path: str,
        backup_path: str,
        language: str,
    ):
        config = Config()
        config.temp_path = temp_path
        config.resource_path = resource_path
        config.genshin_path = genshin_path
        config.mod_sources_path = mod_sources_path
        config.language = language
        config.backup_path = backup_path
        return config

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
        return path.join(
            self.genshin_path,
            "GenshinImpact_Data\\StreamingAssets\\AudioAssets",
        )

    @property
    def sym_path(self) -> str:
        sym = path.join(
            self.genshin_path,
            "GenshinImpact_Data\\StreamingAssets\\AudioAssets",
            self.language,
        )
        return sym

    @staticmethod
    def load():
        if path.isfile("config.json"):
            with open("config.json", "r") as fp:
                return Config.__assign(**json.load(fp))

        conf = Config.__assign(
            temp_path=".\\temp",
            mod_sources_path=".\\resources\\mods",
            resource_path=".\\resources",
            genshin_path="C:\\Program Files\\Genshin Impact\\Genshin Impact game",
            language="Korean",
            backup_path=".\\resources\\backup",
        )
        conf.save()
        return conf

    def save(self):
        with open("config.json", "w") as fp:
            print(json.dump(self.__dict__, fp, indent=2))

    def dump(self) -> str:
        return json.dumps(self.__dict__, indent=2)
