import os
from os import path
from shutil import copyfile, rmtree, copytree, move
from typing import Callable
from tqdm import tqdm

from repack.repack import repack
from config import Config
from Error import (
    ModNameNotValidException,
    ModSourceNotReadyException,
    NoGeneratedModFiles,
)
from src.Error import NotValidPathException


class ModApplier:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.check_mkdirs(config.temp_path)
        self.check_mkdirs(config.resource_path)
        self.check_mkdirs(config.mods_path)
        self.check_mkdirs(config.backup_path)
        self.check_mkdirs(config.applied_mods_path)

        self.input_path = config.backup_path
        pass

    def check_mkdirs(self, dir):
        if not path.isdir(dir):
            os.makedirs(dir)

    def clear_dir(self, dir):
        if path.isdir(dir):
            rmtree(dir)
        os.mkdir(dir)

    def copy_contents(
        self,
        src: str,
        dist: str,
        msg: str | None = None,
        condition: Callable[[str], bool] = lambda file: True,
    ):
        self.check_mkdirs(dist)
        for item in tqdm(os.listdir(src), msg):
            if not condition(item):
                continue
            src_item = path.join(src, item)
            dist_item = path.join(dist, item)
            if path.isdir(src_item):
                copytree(src_item, dist_item)
            else:
                copyfile(src_item, dist_item)

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

    def is_empty_dir(self, dir) -> bool:
        with os.scandir(dir) as it:
            if any(it):
                return False
        return True

    def clear_mod_source(self):
        rmtree(self.config.wem_path)

    def prepare_mod_source(self, source: str) -> int:
        mod_path = path.join(self.config.mods_path, source)
        if not os.listdir(mod_path):
            raise ModNameNotValidException()
        self.copy_contents(mod_path, self.config.wem_path, "preparing mod files")
        return 0

    def set_input_path(self, path: str | None):
        if path is None:
            self.input_path = self.config.backup_path
            return
        self.input_path = path

    def pack_mod_files(self, state: int) -> int:
        config = self.config
        if state != 0 or self.is_empty_dir(config.wem_path):
            raise ModSourceNotReadyException()
        self.clear_dir(config.output_pck_path)
        print("packing mod files")
        repack(
            config.wem_path,
            path.join(self.input_path, config.language),
            config.output_pck_path,
        )

        return 1

    def save_mod_file(self, mod_name: str, state: int):
        if state != 1 or self.is_empty_dir(self.config.output_pck_path):
            raise NoGeneratedModFiles()
        mod_path = path.join(self.config.applied_mods_path, mod_name)
        if path.isdir(mod_path):
            rmtree(mod_path)
        print("save packed mod file")
        move(self.config.output_pck_path, mod_path)

    def apply(self, mod_name: str):
        mod_path = path.join(self.config.applied_mods_path, mod_name)
        if not path.isdir(mod_path):
            raise ModNameNotValidException()

        self.copy_contents(
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
