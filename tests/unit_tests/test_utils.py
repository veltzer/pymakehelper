"""Behavioural tests for pymakehelper's pure file helpers."""

import os
import tempfile
import unittest

from pymakehelper import utils


class GetFlagsTests(unittest.TestCase):
    @staticmethod
    def _write(path: str, content: str) -> None:
        with open(path, "w", encoding="utf-8") as stream:
            stream.write(content)

    def test_parses_flags_line(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            name = os.path.join(d, "f.txt")
            self._write(name, "some text\nFLAGS: a, b ,c\nmore text\n")
            assert utils.get_flags(name) == {"a", "b", "c"}

    def test_no_flags_line_returns_empty_set(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            name = os.path.join(d, "f.txt")
            self._write(name, "nothing here\njust text\n")
            assert utils.get_flags(name) == set()

    def test_multiple_flags_lines_are_unioned(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            name = os.path.join(d, "f.txt")
            self._write(name, "FLAGS: a,b\nFLAGS: b,c\n")
            assert utils.get_flags(name) == {"a", "b", "c"}


class TouchAndDirTests(unittest.TestCase):
    def test_touch_creates_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            name = os.path.join(d, "new.txt")
            assert not os.path.exists(name)
            utils.touch(name)
            assert os.path.isfile(name)

    def test_ensure_dir_creates_parent(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "sub", "deeper", "file.txt")
            utils.ensure_dir(target)
            assert os.path.isdir(os.path.join(d, "sub", "deeper"))

    def test_touch_mkdir_creates_dir_and_file(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "made", "file.txt")
            utils.touch_mkdir(target)
            assert os.path.isfile(target)

    def test_file_gen_non_recursive_lists_files_and_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.txt"), "w", encoding="utf-8"):
                pass
            os.mkdir(os.path.join(d, "sub"))
            (root, directories, files) = next(utils.file_gen(d, recurse=False))
            assert root == d
            assert files == ["a.txt"]
            assert directories == ["sub"]
