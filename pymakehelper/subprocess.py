"""
This module provides a simple wrapper around the subprocess module
"""

import sys
import subprocess
from typing import List
from pymakehelper.configs import ConfigVerbose


def run_no_err(args: List[str]):
    if ConfigVerbose.verbose:
        print(" ".join(args))
    subprocess.call(args)


def run_only_print_on_error(args: List[str]):
    if ConfigVerbose.verbose:
        print(" ".join(args))
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
        out_out, out_err = pr.communicate()
        code = pr.returncode
    if code:
        print(out_out.decode(), end="", file=sys.stdout)
        print(out_err.decode(), end="", file=sys.stderr)
        sys.exit(code)


def run_error_on_print(args: List[str]):
    if ConfigVerbose.verbose:
        print(" ".join(args))
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
        out_out, out_err = pr.communicate()
        _ = pr.returncode
    if len(out_out) > 0 or len(out_err) > 0:
        print(out_out.decode(), end="", file=sys.stdout)
        print(out_err.decode(), end="", file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


def run_error_on_print_or_error(args: List[str]):
    if ConfigVerbose.verbose:
        print(" ".join(args))
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
        out_out, out_err = pr.communicate()
        code = pr.returncode
    if len(out_out) > 0 or len(out_err) > 0 or code:
        print(out_out.decode(), end="", file=sys.stdout)
        print(out_err.decode(), end="", file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)
