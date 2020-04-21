from pytconf.config import register_endpoint, register_function_group

from pymakehelper.configs import ConfigVersion

import pymakehelper

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pymakehelper commands"


def register_group_default():
    register_function_group(
            function_group_name=GROUP_NAME_DEFAULT,
            function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    configs=[
        ConfigVersion,
    ],
    suggest_configs=[
    ],
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pymakehelper.__version__)
