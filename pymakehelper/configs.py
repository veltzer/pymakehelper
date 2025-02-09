"""
All configurations for pymakehelper
"""


from pytconf import Config, ParamCreator


class ConfigVerbose(Config):
    """
    Parameters for verbosity
    """
    verbose = ParamCreator.create_bool(
        help_string="be verbose?",
        default=False,
    )


class ConfigSymlinkInstall(Config):
    """
    Parameters for the symlink install tool
    """
    source_folder = ParamCreator.create_existing_folder(
        help_string="Which folder to install from?",
    )
    target_folder = ParamCreator.create_existing_folder(
        help_string="Which folder to install to?",
    )
    recurse = ParamCreator.create_bool(
        help_string="should I recurse?",
        default=True,
    )
    doit = ParamCreator.create_bool(
        help_string="actually perform the actions?",
        default=True,
    )
    debug = ParamCreator.create_bool(
        help_string="print what we are doing?",
        default=True,
    )
    unlink = ParamCreator.create_bool(
        help_string="remove target files if they are links?",
        default=False,
    )
    incremental = ParamCreator.create_bool(
        help_string="Only do new links?",
        default=True,
    )
    unlink_all = ParamCreator.create_bool(
        help_string="first unlink all targets?",
        default=False,
    )


class ConfigPdflatex(Config):
    """
    Parameters for pdflatex
    """
    input_file = ParamCreator.create_existing_file(
        help_string="input file",
    )
    output_file = ParamCreator.create_new_file(
        help_string="output file",
    )
    remove_tmp = ParamCreator.create_bool(
        help_string="remove the tmp file for output at the end of the run?",
        default=True,
    )
    qpdf = ParamCreator.create_bool(
        help_string="do you want to run the qpdf post processing stage?",
        default=True,
    )
    runs = ParamCreator.create_int(
        help_string="how many times to run pdflatex(1)?",
        default=2,
    )
