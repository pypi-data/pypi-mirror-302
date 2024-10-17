import argparse
import os
import re
import sys
from glob import glob
from importlib.metadata import Distribution
from importlib.metadata import distribution as _get_distribution
from itertools import chain
from pipes import quote
from subprocess import list2cmdline
from typing import Iterable, List, Pattern, Sequence, Set, Tuple

from packaging.requirements import Requirement

from .requirements.utilities import (
    get_distribution,
    get_installed_distributions,
    get_requirements_required_distribution_names,
    get_setup_distribution_name,
    is_installed,
    normalize_name,
)
from .utilities import iter_parse_delimited_values, iter_sys_argv_pop, run

_PROJECT_ROOT_INDICATOR_FILE_NAMES: Set[str] = {
    "setup.cfg",
    "setup.py",
    "pyproject.toml",
}
EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS: Tuple[str, ...] = (
    r"^[.~].*$",
    r"^venv$",
    r"^site-packages$",
)


def _iter_distribution_extras(
    distribution: Distribution,
) -> Iterable[str]:
    if not distribution.requires:
        return
    extras: Set[str] = set()
    requirement: Requirement
    for requirement in map(Requirement, distribution.requires):
        if requirement.marker is not None:
            requirement_marker: str
            for requirement_marker in map(
                str.strip, str(requirement.marker).split(";")
            ):
                variable: str
                operation: str
                value: str
                variable, operation, value = re.split(
                    r"([~<=>\s]+)",
                    requirement_marker,
                    maxsplit=1,
                )
                if variable == "extra":
                    if value not in extras:
                        yield value
                    extras.add(value)


def _get_requirement_string(
    name: str, directory: str, include_extras: bool
) -> str:
    requirement_string: str = os.path.abspath(directory)
    if is_installed(name) and include_extras:
        distribution: Distribution = get_distribution(name)
        extras: Tuple[str, ...] = tuple(
            _iter_distribution_extras(distribution)
        )
        if extras:
            requirement_string = f"{requirement_string}[{','.join(extras)}]"
    return requirement_string


def _iter_find_distributions(
    distribution_names: Set[str],
    directories: Iterable[str] = ("../",),
    exclude_directories: Iterable[str] = (),
    exclude_directory_regular_expressions: Iterable[
        str
    ] = EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS,
    include_extras: bool = False,
) -> Iterable[str]:
    if isinstance(directories, str):
        directories = (directories,)
    directories = map(os.path.abspath, directories)
    exclude_directory_patterns: Tuple[Pattern, ...] = tuple(
        map(re.compile, exclude_directory_regular_expressions)
    )

    def include_directory(directory: str) -> bool:
        if os.path.abspath(directory) in exclude_directories:
            return False
        directory_basename: str = os.path.basename(directory)
        for exclude_directory_pattern in exclude_directory_patterns:
            if exclude_directory_pattern.match(directory_basename):
                return False
        return True

    def iter_find_directory_distributions(directory: str) -> Iterable[str]:
        sub_directories: List[str]
        files: List[str]
        sub_directories, files = next(iter(os.walk(directory)))[1:3]

        def get_subdirectory_path(subdirectory: str) -> str:
            return os.path.join(directory, subdirectory)

        sub_directories = list(map(get_subdirectory_path, sub_directories))
        # Check to see if this is a project directory
        if any(
            map(
                _PROJECT_ROOT_INDICATOR_FILE_NAMES.__contains__,
                map(str.lower, files),
            )
        ):
            name: str = get_setup_distribution_name(directory)
            if name in distribution_names:
                return (
                    _get_requirement_string(name, directory, include_extras),
                )
            else:
                return ()
        else:
            return chain(
                *map(
                    iter_find_directory_distributions,
                    filter(include_directory, sub_directories),
                )
            )

    return chain(*map(iter_find_directory_distributions, directories))


def _get_distribution_major_version(name: str) -> int:
    version: str = ""
    try:
        version = _get_distribution(name).version
    except Exception:
        try:
            version = get_distribution(name).version
        except KeyError:
            pass
    if version:
        return int(version.split(".")[0])
    return -1


def find_and_install_distributions(
    distribution_names: Set[str],
    directories: Iterable[str] = ("../",),
    exclude_directories: Iterable[str] = (),
    exclude_directory_regular_expressions: Iterable[
        str
    ] = EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS,
    dry_run: bool = False,
    include_extras: bool = False,
    pip_install_arguments: Sequence[str] = (),
) -> None:
    """
    Parameters:
    - requirements ([str]) = ():
      One or more requirement specifiers or configuration file paths to which
      installation should be limited
    - directories ([str]) = ("../",): The directories in which to search
      for distributions to install. By default, the parent of the currently
      directory is used.
    - exclude ([str]): One or more distributions to pass over when searching
      for distributable projects
    - exclude_directories ([str]): Glob patterns indicating directories to
      exclude. These patterns may be expressed relative to the current
      directory.
    - exclude_directory_regular_expressions ([str]): Directories with names
      matching any of these patterns will be excluded. This takes into account
      the directory *name* only, and no attempt is made to resolve relative
      paths.
    - dry_run (bool)
    - include_extras (bool)
    - pip_install_arguments ([str]): Additional arguments to pass on to
      `pip install`
    """
    location: str
    exclude_directories = set(
        map(
            os.path.abspath,  # type: ignore
            chain(*map(lambda location: glob(location), exclude_directories)),
        )
    )
    directories = set(
        map(
            os.path.abspath,  # type: ignore
            chain(*map(lambda location: glob(location), directories)),
        )
    )
    requirements: Tuple[str, ...] = tuple(
        _iter_find_distributions(
            distribution_names=distribution_names,
            directories=directories,
            exclude_directory_regular_expressions=(
                exclude_directory_regular_expressions
            ),
            exclude_directories=exclude_directories,
            include_extras=include_extras,
        )
    )
    if requirements:
        command: Tuple[str, ...] = (sys.executable, "-m", "pip", "install")
        # For setuptools version 64, we use compatibility mode to avoid
        # issues with implicit namespace packages and mypy
        if _get_distribution_major_version("setuptools") >= 64:
            command += (
                "--config-settings",
                "editable_mode=compat",
            )
        command += tuple(
            chain(*zip(("-e",) * len(requirements), requirements))
        )
        if pip_install_arguments:
            if isinstance(pip_install_arguments, str):
                pip_install_arguments = (pip_install_arguments,)
            else:
                pip_install_arguments = tuple(pip_install_arguments)
            if (
                "--upgrade-strategy" in pip_install_arguments
                and "-U" not in pip_install_arguments
                and "--upgrade" not in pip_install_arguments
            ):
                pip_install_arguments += ("-U",)
            command += pip_install_arguments
        if dry_run:
            print(list2cmdline(command))
        else:
            run(command)


def install_editable(
    requirements: Iterable[str] = (),
    directories: Iterable[str] = ("../"),
    exclude: Iterable[str] = (),
    exclude_directories: Iterable[str] = (),
    exclude_directory_regular_expressions: Iterable[
        str
    ] = EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS,
    dry_run: bool = False,
    include_extras: bool = False,
    pip_install_arguments: Sequence[str] = (),
) -> None:
    """
    Install, in editable/develop mode, all distributions, except for those
    specified in `exclude`, which are required for the specified
    `requirements`.

    Parameters:
    - requirements ([str]) = ():
      One or more requirement specifiers or configuration file paths to which
      installation should be limited
    - directories ([str]) = ("../",): The directories in which to search
      for distributions to install. By default, the parent of the currently
      directory is used. Glob patterns
    - exclude ([str]): One or more distributions to pass over when searching
      for distributable projects
    - exclude_directories ([str]): Glob patterns of directories to exclude.
      These patterns may be expressed relative to the current directory.
    - exclude_directory_regular_expressions ([str]): Directories with names
      matching any of these patterns will be excluded. This takes into account
      the directory *name* only, and no attempt is made to resolve relative
      paths.
    - dry_run (bool)
    - include_extras (bool)
    - pip_install_arguments ([str]): Additional arguments to pass on to
      `pip install`
    """
    required_distribution_names: Set[str] = (
        get_requirements_required_distribution_names(requirements)
        if requirements
        else set(get_installed_distributions().keys())
    )
    find_and_install_distributions(
        distribution_names=(
            required_distribution_names - set(map(normalize_name, exclude))
        ),
        directories=directories,
        exclude_directories=exclude_directories,
        exclude_directory_regular_expressions=(
            exclude_directory_regular_expressions
        ),
        dry_run=dry_run,
        include_extras=include_extras,
        pip_install_arguments=pip_install_arguments,
    )


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="daves-dev-tools install-editable",
        description=(
            "This command will attempt to find and install, in "
            "develop (editable) mode, all packages which are "
            "installed in the current python environment. If one or "
            "more `requirement` file paths or specifiers are provided, "
            "installation will be limited to the dependencies identified "
            "(recursively) by these requirements. Exclusions can be specified "
            "using the `-e` parameter. Directories can be excluded by "
            "passing regular expressions to the `-edre` parameter. "
            "Any arguments passed not matching those specified below "
            "will be passed on to `pip install` (see `pip install -h` for "
            "additionally available arguments)."
        ),
    )
    parser.add_argument(
        "-r",
        "--requirement",
        action="append",
        type=str,
        default=[],
        help=(
            "One or more requirement specifiers, requirement file paths, "
            "or configuration file paths "
            "(setup.cfg, setup.py, pyproject.toml, tox.ini, etc.). "
            "If provided, only dependencies of these requirements will be "
            "installed."
        ),
    )
    parser.add_argument(
        "-d",
        "--directory",
        default=["../"],
        type=str,
        action="append",
        help=(
            "A directory in which to search for requirements. "
            "By default, the directory above the current directory is "
            "searched. This argument may be passed more than once to include "
            "multiple locations."
        ),
    )
    parser.add_argument(
        "-e",
        "--exclude",
        default=[],
        type=str,
        action="append",
        help="A comma-separated list of distribution names to exclude",
    )
    parser.add_argument(
        "-ed",
        "--exclude-directory",
        default=[],
        type=str,
        action="append",
        help=(
            "One or more glob patterns indicating directories to exclude. "
            "This argument may be expressed as a path relative to the current."
        ),
    )
    parser.add_argument(
        "-edre",
        "--exclude-directory-regular-expression",
        default=list(EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS),
        type=str,
        action="append",
        help=(
            "Directories matching this regular expression will be excluded "
            "when searching for setup locations This argument may be passed "
            "more than once to exclude directories matching more than one "
            "regular expression. The default for this argument is "
            "equivalent to `-edre {}`. Unlike for *--exclude-directory*, "
            "these expressions apply only to the directory *name*, and "
            "no attempt to resolve relative paths is made.".format(
                " -edre ".join(
                    map(quote, EXCLUDE_DIRECTORY_REGULAR_EXPRESSIONS)
                )
            )
        ),
    )
    parser.add_argument(
        "-dr",
        "--dry-run",
        default=False,
        action="store_const",
        const=True,
        help="Print, but do not execute, all `pip install` commands",
    )
    parser.add_argument(
        "-ie",
        "--include-extras",
        default=False,
        action="store_const",
        const=True,
        help="Install all extras for all discovered distributions",
    )
    # For backwards compatibility, we accept requirements as either
    # positional or keyword arguments
    positional_arguments: List[str] = list(iter_sys_argv_pop())
    namespace: argparse.Namespace
    unknown_arguments: List[str]
    namespace, unknown_arguments = parser.parse_known_args()
    install_editable(
        requirements=namespace.requirement + positional_arguments,
        directories=namespace.directory,
        exclude_directory_regular_expressions=(
            namespace.exclude_directory_regular_expression
        ),
        exclude_directories=namespace.exclude_directory,
        exclude=iter_parse_delimited_values(namespace.exclude),
        dry_run=namespace.dry_run,
        include_extras=namespace.include_extras,
        pip_install_arguments=unknown_arguments,
    )


if __name__ == "__main__":
    main()
