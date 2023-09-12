import os
from os import path
from shutil import rmtree, move

from .repack.repack import repack
from .config import Config
from .utils.error import (
    ModNameNotValidException,
    ModSourceNotReadyException,
    NotValidPathException,
)


from .utils.dir import check_mkdirs, is_empty_dir, clear_dir, copy_contents


class ModTool:
    def __init__(self, config: Config) -> None:
        self.config = config
        check_mkdirs(config.temp_path)
        check_mkdirs(config.resource_path)
        check_mkdirs(config.mod_sources_path)
        check_mkdirs(config.backup_path)
        check_mkdirs(config.packed_mods_path)

        self.input_path = config.backup_path
        pass

    # Step 1 : backup
    def move_and_link_original(self):
        if path.islink(self.config.sym_path) or not path.isdir(self.config.sym_path):
            raise NotValidPathException(
                "selected language is Not installed or Already Linked"
            )
        lang_backup = path.join(self.config.backup_path, self.config.language)
        if path.exists(lang_backup):
            rmtree(lang_backup)
        print("backup original sound files")
        move(self.config.sym_path, self.config.backup_path)
        os.symlink(lang_backup, self.config.sym_path, True)

    # region Step 2 : mod source insert
    def set_input_path(self, input_path: str | None = None):
        if input_path is None:
            self.input_path = path.join(self.config.backup_path, self.config.language)
            return
        self.input_path = input_path

    def clear_mod_source(self):
        rmtree(self.config.wem_path)

    def prepare_mod_source(self, source: str) -> int:
        mod_path = path.join(self.config.mod_sources_path, source)
        if not os.listdir(mod_path):
            raise ModNameNotValidException()
        copy_contents(mod_path, self.config.wem_path, "preparing mod files")
        return 0

    # endregion

    # Step 3 : generate mod files

    def pack_mod_files(self, mod_name: str, state: int):
        config = self.config

        mod_path = path.join(self.config.packed_mods_path, mod_name)
        if path.isdir(mod_path):
            rmtree(mod_path)

        if state != 0 or is_empty_dir(config.wem_path):
            raise ModSourceNotReadyException()
        clear_dir(mod_path)
        print("packing mod files")
        repack(
            config.wem_path,
            self.input_path,
            mod_path,
        )
        print("save packed mod file")

    # Step 4 : Apply Mod
    def apply(self, mod_name: str):
        mod_path = path.join(self.config.packed_mods_path, mod_name)
        if not path.isdir(mod_path):
            raise ModNameNotValidException()

        copy_contents(
            path.join(self.config.backup_path, self.config.language),
            mod_path,
            "copying missing files",
            lambda file: not path.exists(path.join(mod_path, file)),
        )
        print("make symlink")
        if path.islink(self.config.sym_path):
            os.unlink(self.config.sym_path)
        os.symlink(mod_path, self.config.sym_path)

    def restore(self, link=True):
        if path.islink(self.config.sym_path):
            os.unlink(self.config.sym_path)
        origin = path.join(self.config.backup_path, self.config.language)
        sym = self.config.sym_path

        if link:
            os.symlink(origin, sym)
        else:
            move(origin, sym)

