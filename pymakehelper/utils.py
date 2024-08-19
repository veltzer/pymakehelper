import logging
import os
import subprocess

from pymakehelper.static import APP_NAME
from pymakehelper.configs import ConfigSymlinkInstall


def ensure_dir(f, exist_ok=True):
    folder = os.path.dirname(f)
    if folder != "":
        os.makedirs(folder, exist_ok=exist_ok)


def touch(f):
    if os.path.isfile(f):
        os.utime(f, None)
    else:
        with open(f, "w"):
            pass


def touch_mkdir(f):
    ensure_dir(f)
    touch(f)


def touch_mkdir_many(filenames):
    for filename in filenames:
        touch_mkdir(filename)


def no_err_run(args):
    subprocess.call(args)


def get_logger():
    return logging.getLogger(APP_NAME)


def do_real_install(source, target):
    """ This does the real installation """
    logger = get_logger()
    if ConfigSymlinkInstall.unlink:
        if os.path.islink(target):
            logger.info(f"unlinking [{target}]")
            os.unlink(target)
    if ConfigSymlinkInstall.doit:
        logger.info(f"symlinking [{source}], [{target}]")
        os.symlink(source, target)


def do_install(source, target):
    """install a single symlink"""
    logger = get_logger()
    if ConfigSymlinkInstall.incremental:
        if os.path.exists(target):
            assert os.path.islink(target)
            if os.readlink(target) != source:
                logger.info(f"unlinking [{target}]")
                os.unlink(target)
                do_real_install(source, target)
        else:
            do_real_install(source, target)
    else:
        do_real_install(source, target)


def file_gen(root_folder: str, recurse: bool):
    """generate all files in a folder"""
    if recurse:
        yield from os.walk(root_folder)
    else:
        directories = []
        files = []
        for file in os.listdir(root_folder):
            full = os.path.join(root_folder, file)
            if os.path.isdir(full):
                directories.append(file)
            if os.path.isfile(full):
                files.append(file)
        yield root_folder, directories, files
