"""
This is a script that runs pdflatex for us.
Why do we need this script ?
- to remove the output before we run pdflatex so that we will be sure that we start clean.
if pdflatex finds a file it will * reprocess * it and we dont want that, do we ?
- we need to run pdflatex twice to create indexes and more.
- pdf latex is way too verbose - we want to remove that output and only show it if there is
an error.
- in case we fail we want to make sure we remove the output.

Maybe more reasons will follow...

Take note of the argument we pass to pdflatex:
- -interaction=nonstopmode - this means that latex will not stop and enter interactive
mode to ask the user what to do about an error (what is this behaviour anyway ?!?).
- -halt-on-error - this means that latex will stop on error.
- -output-directory - this tells pdflatex where the output folder is.

This python script is a rewrite of a similar script in perl.
"""

import sys
import os
import os.path
from pymakehelper.configs import ConfigPdflatex, ConfigVerbose
from pymakehelper.subprocess import run_only_print_on_error
from pymakehelper.utils import unlink_check


def printout(filename: str):
    """
    print to stdout a file content
    this function is adjusted for the ugly output that pdflatex produces and so it
    only prints the lines between lines starting with "!" (including the actual lines
    starting with "!"). Apparently this is how pdflatex shows errors. Ugrrr...
    """
    if ConfigVerbose.verbose:
        print(f"printing [{filename}]", file=sys.stderr)
    with open(filename, encoding="UTF8") as file:
        inerr = False
        for line in file:
            if inerr:
                print(line, file=sys.stderr)
                inerr = False
            else:
                if line.startswith("!"):
                    print(line, file=sys.stderr)
                    inerr = True


def chmod_check(filename: str, check: bool):
    """
    this is a function that chmods a file and can optionally die if there is a problem
    """
    if ConfigVerbose.verbose:
        print(f"chmodding [{filename}]", file=sys.stderr)
    if check:
        os.chmod(filename, 0o444)
    else:
        try:
            os.chmod(filename, 0o444)
        # pylint: disable=broad-exception-caught
        except Exception:
            pass


def my_rename(old_filename: str, new_filename: str, check: bool):
    """
    this is a function that renames a file and dies if there is a problem
    """
    if ConfigVerbose.verbose:
        print(f"my_rename [{old_filename, new_filename}]", file=sys.stderr)
    if check:
        os.rename(old_filename, new_filename)
    else:
        try:
            os.rename(old_filename, new_filename)
        # pylint: disable=broad-exception-caught
        except Exception:
            pass


def run_wrapper_pdflatex():
    """ main entry point """
    filename_input = ConfigPdflatex.input_file
    filename_output = ConfigPdflatex.output_file
    output_dir = os.path.dirname(filename_output)
    output_base = os.path.splitext(filename_output)[0]

    args = [
        "pdflatex",
        "-shell-escape",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory",
        output_dir,
        filename_input,
    ]
    if ConfigVerbose.verbose:
        print(f"input is [{filename_input}]")
        print(f"output is [{filename_output}")
        print(f"cmd is [{args}")
    # first remove the output (if it exists)
    unlink_check(
        filename_output,
    )
    # we need to run the command twice!!! (to generate the index and more)
    for _ in range(ConfigPdflatex.runs):
        run_only_print_on_error(args)
        unlink_check(output_base + ".log")
        unlink_check(output_base + ".out")
        unlink_check(output_base + ".toc")
        unlink_check(output_base + ".aux")
        unlink_check(output_base + ".nav")
        unlink_check(output_base + ".snm")
        unlink_check(output_base + ".vrb")

    if ConfigPdflatex.qpdf:
        # move the output to the new place
        tmp_output = filename_output + ".tmp"
        my_rename(filename_output, tmp_output, True)
        # I also had "--force-version=1.5" but it is not needed since I use
        # pdflatex and pdftex with the right version there...
        args = [
            "qpdf",
            "--deterministic-id",
            "--linearize",
            tmp_output,
            filename_output,
        ]
        run_only_print_on_error(args)
        unlink_check(tmp_output)
