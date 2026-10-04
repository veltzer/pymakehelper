# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pymakehelper/wrapper_pdflatex.py:88` - `output_dir`/`output_base` are derived from `--output_file`, but pdflatex names its output after the input's job name (`<input-basename>.pdf` in `-output-directory`); when the two basenames differ the output file is never produced at the expected path, the qpdf rename at line 122 fails, and the `.log/.aux/...` cleanup at lines 111-117 deletes the wrong names. Pass `-jobname` derived from `output_file` (or validate the basenames match).
- `src/pymakehelper/main.py:46` - `unlink_all` compares `os.path.realpath(full)` (absolute) against the raw `ConfigSymlinkInstall.source_folder`, before it is made absolute at lines 52-55; with a relative `--source_folder` nothing is ever unlinked. It is also a plain string prefix test, so `/a/src` matches links into `/a/src2`. Resolve `source_folder` with `realpath` first and compare with `os.path.commonpath`.

## Medium

- `src/pymakehelper/wrapper_pdflatex.py:93` - pdflatex is always run with `-shell-escape`, which lets any processed `.tex` file execute arbitrary shell commands; make it an opt-in `ConfigPdflatex` flag (default off) and mention it in the module docstring's argument list (lines 13-17), which currently omits it.
- `src/pymakehelper/main.py:75` - `symlink_install` creates target directories with `os.mkdir` even when `--doit` is false, so the dry-run flag is not honoured; guard the mkdir (and the `unlink` in `utils.py:70`) with `ConfigSymlinkInstall.doit`.
- `src/pymakehelper/utils.py:67` - `assert os.path.islink(target)` is used to validate user filesystem state (also `main.py:72`); asserts vanish under `python -O` and give a bare `AssertionError` otherwise. Raise a real error with the offending path.
- `src/pymakehelper/main.py:49` - `os.mkdir(target_folder)` is unreachable: `target_folder` is declared with `ParamCreator.create_existing_folder` (`configs.py:26`), so pytconf rejects a missing folder before this runs. Either switch the param to a plain folder param (which is what `doc/TODO.txt:7` asks for) or delete the dead branch.

## Low

- `src/pymakehelper/wrapper_pdflatex.py:31` - `printout()` and `chmod_check()` (line 52) are never called anywhere, and `my_rename()` is only ever called with `check=True`; remove the dead code and the swallowed-exception branches it carries. `printout()` would also double-space output because it prints lines that already end in `\n` (lines 44, 48).
- `src/pymakehelper/configs.py:37` - `ConfigSymlinkInstall.debug` is defined but never read; remove it or wire it to the logger level.
- `src/pymakehelper/wrapper_pdflatex.py:102` - verbose f-strings are missing the closing `]` (`output is [...`, `cmd is [...` at line 103).
- `src/pymakehelper/main.py:132` - typo "programin" in the `error_on_print_or_error` endpoint description shown in `--help`.
- `doc/TODO.txt:1` - stale: the `pymakehelper.subprocess` module exists and `wrapper_pdflatex` uses it, `touch_mkdir` covers the `mkdir_for` item (line 10), and `--incremental` implements most of the "smarter symlink install" item (line 14); prune what is done.
- `pyproject.toml:86` - `mypy_path = "src:python:scripts"` names `python/` and `scripts/`, which do not exist; use `"src"`.
- `rsconstruct.toml:28` - `[processor.ruff]` and `[processor.mypy]` (line 32) list `config`, which holds only Lua files; drop it.
- `.yamllint.yaml` - the shared yamllint config is present but `rsconstruct.toml` has no `[processor.yamllint]`, so `.github/*.yml` is never yamllint-checked; add the processor with precise `src_dirs`/`src_files` (do not delete the shared file).
- `tests/unit_tests/test_utils.py:1` - tests cover only the file helpers; `symlink_install`, `do_install`, and the subprocess wrappers (exit-code logic in `subprocess.py:29-54`, `reverse_exitcode` in `main.py:151`) have no tests, which is where the bugs above live.
