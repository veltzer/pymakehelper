"""
main file
"""

import os  # for walk, getcwd, symlink, listdir, unlink, mkdir
import os.path  # for join, expanduser, realpath, abspath, islink, isdir, isfile
import subprocess
import sys

import pylogconf.core
from pytconf import register_endpoint, get_free_args, config_arg_parse_and_launch, \
    register_main

from pymakehelper.configs import ConfigSymlinkInstall
from pymakehelper.static import DESCRIPTION, APP_NAME, VERSION_STR
from pymakehelper.utils import touch_mkdir_many, no_err_run, debug, do_install, file_gen


@register_endpoint(
    description="Install symlinks to things in a folder",
    configs=[
        ConfigSymlinkInstall,
    ],
)
def symlink_install() -> None:
    cwd = os.getcwd()
    # first unlink all paths in target leading back to here
    if os.path.isdir(ConfigSymlinkInstall.target_folder):
        for file in os.listdir(ConfigSymlinkInstall.target_folder):
            full = os.path.join(ConfigSymlinkInstall.target_folder, file)
            if os.path.islink(full):
                link_target = os.path.realpath(full)
                if link_target.startswith(cwd):
                    if ConfigSymlinkInstall.doit:
                        debug('unlinking [{0}]'.format(full))
                        os.unlink(full)
    else:
        os.mkdir(ConfigSymlinkInstall.target_folder)
    # now create the new links
    for root, directories, files in file_gen(ConfigSymlinkInstall.source_folder, ConfigSymlinkInstall.recurse):
        for file in files:
            source = os.path.abspath(os.path.join(root, file))
            target = os.path.join(ConfigSymlinkInstall.target_folder, file)
            do_install(source, target, ConfigSymlinkInstall.force, ConfigSymlinkInstall.doit)
        for directory in directories:
            source = os.path.abspath(os.path.join(root, directory))
            target = os.path.join(ConfigSymlinkInstall.target_folder, directory)
            do_install(source, target, ConfigSymlinkInstall.force, ConfigSymlinkInstall.doit)


@register_endpoint(
    description="Remove one folder from each file name",
    allow_free_args=True,
)
def remove_folders() -> None:
    result = []
    for filename in get_free_args():
        r = os.sep.join(filename.split(os.sep)[1:])
        result.append(r)
    print(' '.join(result), end='')


@register_endpoint(
    description="Touch a folder, possibly creating folders for it",
    allow_free_args=True,
)
def touch_mkdir() -> None:
    touch_mkdir_many(get_free_args())


@register_endpoint(
    description="Return with no error even if underlying process returns error",
    allow_free_args=True,
)
def no_err() -> None:
    no_err_run(get_free_args())


@register_endpoint(
    description="Collect stdout and stderr and print them only in error",
    allow_free_args=True,
)
def only_print_on_error() -> None:
    if ConfigSymlinkInstall.print_command:
        print(" ".join(get_free_args()))
    pr = subprocess.Popen(get_free_args(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out_out, out_err) = pr.communicate()
    status = pr.returncode
    if status:
        print(out_out.decode(), end='')
        print(out_err.decode(), end='')
        sys.exit(status)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
