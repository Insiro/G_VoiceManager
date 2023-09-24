import os
from os import path
from shutil import copyfile, copytree, rmtree
from typing import Callable

from tqdm import tqdm


def is_empty_dir(dir) -> bool:
    with os.scandir(dir) as it:
        if any(it):
            return False
    return True


def check_mkdirs(dir):
    if not path.isdir(dir):
        os.makedirs(dir)


def clear_dir(dir):
    if path.isdir(dir):
        rmtree(dir)
    os.mkdir(dir)


def copy_contents(
    src: str,
    dist: str,
    msg: str | None = None,
    condition: Callable[[str], bool] = lambda file: True,
):
    check_mkdirs(dist)
    for item in tqdm(os.listdir(src), msg):
        if not condition(item):
            continue
        src_item = path.join(src, item)
        dist_item = path.join(dist, item)
        if path.islink(dist_item):
            os.unlink(dist_item)

        if path.isdir(src_item):
            copytree(src_item, dist_item)
        else:
            copyfile(src_item, dist_item)


def link_contents(
    src: str,
    dist: str,
    msg: str | None = None,
    condition: Callable[[str], bool] = lambda file: True,
):
    check_mkdirs(dist)
    for item in tqdm(os.listdir(src), msg):
        src_item = path.abspath(path.join(src, item))
        dist_item = path.join(dist, item)
        if path.isfile(src_item):
            link_file(src_item, dist_item, condition)
            continue
        link_folder(src_item, dist_item, condition)


def link_folder(
    src: str, dist: str, condition: Callable[[str], bool] = lambda file: True
):
    if not path.isdir(dist):
        os.makedirs(dist)
    for item in os.listdir(src):
        src_item = path.join(src, item)
        dist_item = path.join(dist, item)
        link_file(src_item, dist_item, condition)


def link_file(
    src: str, dist: str, condition: Callable[[str], bool] = lambda file: True
):
    src_name = path.basename(src)
    if path.islink(dist):
        os.unlink(dist)
    elif not condition(src_name):
        return
    os.symlink(src, dist)
