import os
from os import path
from shutil import rmtree, move

from .repack.repack import repack
from .config import Config
from .utils.error import (
    ModNameNotValidException,
    ModSourceNotReadyException,
    NoGeneratedModFiles,
    NotValidPathException,
)


from .utils.dir import check_mkdirs, is_empty_dir, clear_dir, copy_contents


class ModTool:
    def __init__(self, config: Config) -> None:
        self.config = config
        check_mkdirs(config.temp_path)
        check_mkdirs(config.resource_path)
        check_mkdirs(config.mods_path)
        check_mkdirs(config.backup_path)
        check_mkdirs(config.applied_mods_path)

        self.input_path = config.backup_path
        pass

    # Step 1 : backup
    def move_and_link_original(self):
        if path.islink(self.config.sym_path):
            raise NotValidPathException(
                "selected language is Not installed or Already Linked"
            )
        lang_backup = path.join(self.config.backup_path, self.config.language)
        if path.exists(lang_backup):
            rmtree(lang_backup)
        print("backup original sound files")
        move(self.config.sym_path, self.config.backup_path)
        os.symlink(self.config.sym_path, self.config.backup_path)

    # region Step 2 : mod source insert
    def set_input_path(self, path: str | None):
        if path is None:
            self.input_path = self.config.backup_path
            return
        self.input_path = path

    def clear_mod_source(self):
        rmtree(self.config.wem_path)

    def prepare_mod_source(self, source: str) -> int:
        mod_path = path.join(self.config.mods_path, source)
        if not os.listdir(mod_path):
            raise ModNameNotValidException()
        copy_contents(mod_path, self.config.wem_path, "preparing mod files")
        return 0

    # endregion

    # region Step 3 : generate mod files
    def pack_mod_files(self, state: int) -> int:
        config = self.config
        if state != 0 or is_empty_dir(config.wem_path):
            raise ModSourceNotReadyException()
        clear_dir(config.output_pck_path)
        print("packing mod files")
        repack(
            config.wem_path,
            path.join(self.input_path, config.language),
            config.output_pck_path,
        )

        return 1

    def save_mod_file(self, mod_name: str, state: int):
        if state != 1 or is_empty_dir(self.config.output_pck_path):
            raise NoGeneratedModFiles()
        mod_path = path.join(self.config.applied_mods_path, mod_name)
        if path.isdir(mod_path):
            rmtree(mod_path)
        print("save packed mod file")
        move(self.config.output_pck_path, mod_path)

    # endregion
    # Step 4 : Apply Mod
    def apply(self, mod_name: str):
        mod_path = path.join(self.config.applied_mods_path, mod_name)
        if not path.isdir(mod_path):
            raise ModNameNotValidException()

        copy_contents(
            path.join(self.config.backup_path, self.config.language),
            mod_path,
            "coping missing files",
            lambda file: not path.exists(path.join(mod_path, file)),
        )
        print("make symlink")
        if path.islink(self.config.sym_path):
            os.unlink(self.config.sym_path)
        os.symlink(mod_path, self.config.sym_path)

    def restore(self):
        pass