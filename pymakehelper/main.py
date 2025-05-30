"""
main file
"""

import os  # for walk, symlink, listdir, unlink, mkdir
import os.path  # for join, expanduser, realpath, abspath, islink, isdir, isfile
import subprocess
import sys

import pylogconf.core
from pytconf import register_endpoint, get_free_args, config_arg_parse_and_launch, \
    register_main

from pymakehelper.configs import ConfigSymlinkInstall, ConfigVerbose
from pymakehelper.static import DESCRIPTION, APP_NAME, VERSION_STR
from pymakehelper.utils import touch_mkdir_many, get_logger, do_install, file_gen, get_flags
from pymakehelper.subprocess import run_error_on_print_or_error, run_no_err, run_only_print_on_error
from pymakehelper.wrapper_pdflatex import run_wrapper_pdflatex
from pymakehelper.configs import ConfigPdflatex
from pymakehelper.subprocess import run_error_on_print


@register_endpoint(
    description="Run pdflatex",
    configs=[
        ConfigPdflatex,
        ConfigVerbose,
    ],
)
def wrapper_pdflatex() -> None:
    run_wrapper_pdflatex()


@register_endpoint(
    description="Install symlinks to things in a folder",
    configs=[
        ConfigSymlinkInstall,
        ConfigVerbose,
    ],
)
def symlink_install() -> None:
    logger = get_logger()
    # first unlink all paths in target leading back to here
    if ConfigSymlinkInstall.unlink_all:
        if os.path.isdir(ConfigSymlinkInstall.target_folder):
            for filename in os.listdir(ConfigSymlinkInstall.target_folder):
                full = os.path.join(ConfigSymlinkInstall.target_folder, filename)
                if os.path.islink(full):
                    link_target = os.path.realpath(full)
                    if link_target.startswith(ConfigSymlinkInstall.source_folder):
                        if ConfigSymlinkInstall.doit:
                            logger.info(f"unlinking [{full}]")
                            os.unlink(full)
    if not os.path.isdir(ConfigSymlinkInstall.target_folder):
        os.mkdir(ConfigSymlinkInstall.target_folder)
    # convert to abs path
    if os.path.isabs(ConfigSymlinkInstall.source_folder):
        source_folder = ConfigSymlinkInstall.source_folder
    else:
        source_folder = os.path.abspath(ConfigSymlinkInstall.source_folder)
    if os.path.isabs(ConfigSymlinkInstall.target_folder):
        target_folder = ConfigSymlinkInstall.target_folder
    else:
        target_folder = os.path.abspath(ConfigSymlinkInstall.target_folder)
    # now create the new links
    for dirname, directories, files in file_gen(source_folder, ConfigSymlinkInstall.recurse):
        for file in files:
            source = os.path.join(dirname, file)
            diff = source[len(source_folder) + 1:]
            target = os.path.join(target_folder, diff)
            do_install(source, target)
        for directory in directories:
            source = os.path.abspath(os.path.join(dirname, directory))
            diff = source[len(source_folder) + 1:]
            target = os.path.join(target_folder, diff)
            if os.path.exists(target):
                assert os.path.isdir(target)
            else:
                logger.info(f"os.mkdir [{target}]")
                os.mkdir(target)
            # do_install(source, target)


@register_endpoint(
    description="Remove one folder from each file name",
    allow_free_args=True,
)
def remove_folders() -> None:
    result = []
    for filename in get_free_args():
        r = os.sep.join(filename.split(os.sep)[1:])
        result.append(r)
    print(" ".join(result), end="")


@register_endpoint(
    description="Touch a file, possibly creating folders for it",
    allow_free_args=True,
)
def touch_mkdir() -> None:
    touch_mkdir_many(get_free_args())


@register_endpoint(
    description="Return with no error even if underlying process returns error",
    allow_free_args=True,
)
def no_err() -> None:
    run_no_err(get_free_args())


@register_endpoint(
    description="Collect stdout and stderr and print them only when the program returns error",
    allow_free_args=True,
    min_free_args=1,
    configs=[
        ConfigVerbose,
    ],
)
def only_print_on_error() -> None:
    run_only_print_on_error(get_free_args())


@register_endpoint(
    description="disregard exit code of command and issue error if there is stdout or stderr output",
    allow_free_args=True,
    min_free_args=1,
    configs=[
        ConfigVerbose,
    ],
)
def error_on_print() -> None:
    run_error_on_print(get_free_args())


@register_endpoint(
    description="if the programin returns an error or prints anything issue an error print",
    allow_free_args=True,
    min_free_args=1,
    configs=[
        ConfigVerbose,
    ],
)
def error_on_print_or_error() -> None:
    run_error_on_print_or_error(get_free_args())


@register_endpoint(
    description="reverse the exitcode of a command",
    allow_free_args=True,
    min_free_args=1,
    configs=[
        ConfigVerbose,
    ],
)
def reverse_exitcode() -> None:
    if ConfigVerbose.verbose:
        print(" ".join(get_free_args()))
    exitcode = subprocess.call(get_free_args())
    sys.exit(int(not bool(exitcode)))


@register_endpoint(
    description="run a build",
    allow_free_args=True,
    min_free_args=0,
)
def run_make() -> None:
    if not os.path.isfile("Makefile"):
        return
    if os.path.isfile(".build.disable"):
        return
    args = ["make"]
    args.extend(get_free_args())
    subprocess.check_call(args)


@register_endpoint(
    description="run command with options of ignore",
    allow_free_args=True,
    min_free_args=3,
)
def run_with_ignore() -> None:
    args = get_free_args()
    filename = args[0]
    flag = args[1]
    cmd = args[2:]
    flags = get_flags(filename)
    if flag in flags:
        sys.exit(0)
    subprocess.check_call(cmd)


@register_endpoint(
    description="wrap css validation command line",
    allow_free_args=True,
    min_free_args=1,
)
def wrapper_css_validator() -> None:
    args = get_free_args()
    out = subprocess.check_output(args).decode()
    do_print = False
    error = False
    for line in out.split("\n"):
        if line.startswith("Sorry"):
            do_print = True
            error = True
        if line.startswith("Valid"):
            do_print = False
        if do_print:
            print(line)
    if error:
        sys.exit(1)


@register_endpoint(
    description="print the environment variables pymakehelper is using",
)
def env() -> None:
    print(os.environ)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == "__main__":
    main()
