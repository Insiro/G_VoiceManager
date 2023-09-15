import os
from os import path
from shutil import rmtree, move

from ..repack.repack import repack
from ..config import Config
from ..utils.error import NotValidPathException


from ..utils.dir import check_mkdirs, clear_dir, copy_contents, link_contents


class ModTool:
    input_path: str
    input_changed = False

    def __init__(self, config: Config) -> None:
        self.config = config
        check_mkdirs(config.temp_path)
        check_mkdirs(config.resource_path)
        check_mkdirs(config.mod_sources_path)
        check_mkdirs(config.backup_path)
        check_mkdirs(config.packed_mods_path)

        self.reset_input_path()
        pass

    # Step 1 : backup
    def move_and_link_original(self):
        if not path.isdir(self.config.sym_path):
            raise NotValidPathException("selected language is Not installed")
        lang_backup = path.join(self.config.backup_path, self.config.voice_lang)
        if path.exists(lang_backup):
            rmtree(lang_backup)
        print("--------backup original sound files------")
        move(self.config.sym_path, self.config.backup_path)
        os.symlink(lang_backup, self.config.sym_path, True)

    # region Step 2 : mod source insert
    def reset_input_path(self):
        self.input_changed = False
        self.input_path = path.join(self.config.backup_path, self.config.voice_lang)

    def set_input_path(self, input_path: str):
        self.input_changed = True
        self.input_path = input_path

    def clear_mod_source(self):
        rmtree(self.config.wem_path)

    def prepare_mod_source(self, source_path: str):
        copy_contents(source_path, self.config.wem_path, "preparing mod files")

    # endregion

    # Step 3 : generate mod files

    def pack_mod_files(self, mod_path: str):
        clear_dir(mod_path)
        print("packing mod files")
        repack(
            self.config.wem_path,
            self.input_path,
            mod_path,
        )
        print("save packed mod file")

    # Step 4 : Apply Mod
    def apply(self, mod_path: str):
        lang_backup_path = path.join(self.config.backup_path, self.config.voice_lang)
        if self.input_changed:
            copy_contents(
                lang_backup_path,
                mod_path,
                "copying missing files",
                lambda file: file.startswith("External")
                and not path.exists(path.join(mod_path, file)),
            )
        if path.islink(self.config.sym_path):
            os.unlink(self.config.sym_path)
        link_contents(
            lang_backup_path,
            mod_path,
            "linking other files",
            lambda file: not path.exists(path.join(mod_path, file)),
        )
        os.symlink(path.abspath(mod_path), self.config.sym_path)

    def restore(self, link=True):
        os.unlink(self.config.sym_path)
        origin = path.abspath(
            path.join(self.config.backup_path, self.config.voice_lang)
        )
        sym = self.config.sym_path

        if link:
            os.symlink(origin, sym)
        else:
            move(origin, sym)
