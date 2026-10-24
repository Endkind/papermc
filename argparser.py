import argparse


def get_default_argparse(description: str):
    parser = argparse.ArgumentParser(description=description)

    verbosity_group = parser.add_mutually_exclusive_group()

    verbosity_group.add_argument(
        "--verbose",
        "-v",
        dest="verbosity",
        action="store_const",
        const=2,
        default=1,
        help="Enable debug output.",
    )

    verbosity_group.add_argument(
        "--quiet",
        "-q",
        dest="verbosity",
        action="store_const",
        const=0,
        help="Show warnings and errors only.",
    )

    return parser
