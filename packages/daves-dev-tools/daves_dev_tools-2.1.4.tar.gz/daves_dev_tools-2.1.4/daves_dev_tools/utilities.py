import functools
import os
import runpy
import sys
from collections import deque
from itertools import chain
from shutil import which
from subprocess import check_output, list2cmdline
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    NoReturn,
    Optional,
    Sequence,
    Set,
    Union,
    overload,
)
from urllib.parse import ParseResult
from urllib.parse import quote as _quote
from urllib.parse import urlparse, urlunparse

__all__: List[str] = [
    "lru_cache",
    "run",
    "iter_parse_delimited_values",
    "iter_sys_argv_pop",
    "sys_argv_pop",
    "iter_sys_argv_get",
    "sys_argv_get",
    "update_url_user_password",
]
lru_cache: Callable[..., Any] = functools.lru_cache


def update_url_user_password(
    url: str,
    user: str,
    password: str = "",
    quote: Callable[[str], str] = _quote,
) -> str:
    """
    Update a URL's user and password and return the result.

    Parameters:

    - url (str)
    - user (str)
    - password (str) = "": (optional)
    - quote = urllib.parse.quote: A function to use for escaping
      invalid character (defaults to `urllib.parse.quote`)
    """
    assert url and user
    parse_result: ParseResult = urlparse(url)
    host: str = parse_result.netloc.rpartition("@")[-1]
    user_password: str = quote(user)
    if password:
        user_password = f"{user_password}:{quote(password)}"
    return urlunparse(
        (
            parse_result.scheme,
            f"{user_password}@{host}",
            parse_result.path,
            parse_result.params,
            parse_result.query,
            parse_result.fragment,
        )
    )


def _iter_parse_delimited_value(value: str, delimiter: str) -> Iterable[str]:
    return value.split(delimiter)


def iter_parse_delimited_values(
    values: Iterable[str], delimiter: str = ","
) -> Iterable[str]:
    """
    This function iterates over input values which have been provided as a
    list or iterable and/or a single string of character-delimited values.
    A typical use-case is parsing multi-value command-line arguments.
    """
    if isinstance(values, str):
        values = (values,)

    def iter_parse_delimited_value_(value: str) -> Iterable[str]:
        return _iter_parse_delimited_value(value, delimiter=delimiter)

    return chain(*map(iter_parse_delimited_value_, values))


def run(command: Sequence[str], echo: bool = True, input: str = "") -> str:
    """
    This function runs a shell command, raises an error if a non-zero
    exit code is returned, and echo's both the command and output *if*
    the `echo` parameter is `True`.

    Parameters:

    - command (str|[str]): A shell command
    - echo (bool) = True: If `True`, the command and the output from the
      command will be printed to stdout
    - input (str)
    """
    if command and not isinstance(command, str):
        path: Optional[str] = which(command[0])
        if path:
            command = (path,) + tuple(command[1:])
    if echo:
        command_str: str
        if isinstance(command, str):
            command_str = command
        else:
            command_str = list2cmdline(command)
        print(command_str)
    output: str = check_output(  # type: ignore
        command,
        encoding="utf-8",
        universal_newlines=True,
        shell=isinstance(command, str),
        **dict(filter(all, (("input", input),))),
    ).strip()
    if echo:
        try:
            print(output)
        except UnicodeEncodeError:
            encoding: str = sys.getdefaultencoding()
            if encoding == "utf-8":
                raise
            else:
                print(
                    str(
                        output.encode(encoding=encoding, errors="replace"),
                        encoding=encoding,
                        errors="replace",
                    )
                )
    return output


def _dummy_sys_exit(__status: object) -> None:
    return


def run_module_as_main(
    module_name: str,
    arguments: Sequence[str] = (),
    directory: str = ".",
    echo: bool = False,
) -> None:
    """
    This function runs a module as a main entry point, effectively as a CLI,
    but in the same sub-process as the calling function (thereby retaining
    all privileges granted to the current sub-process).

    Parameters:

    - module_name (str)
    - arguments ([str]) = (): The system arguments to pass to this command,
      replacing `sys.argv` while running the module).
    - directory (str) = ".": The directory in which the command should
      be executed (replacing `os.path.curdir` while running the module).
    - echo (bool) = False: If `True`, an equivalent shell command is printed
      to sys.stdout.
    """
    prior_sys_exit: Callable[[Union[str, int, None]], NoReturn] = sys.exit
    prior_sys_argv: List[str] = sys.argv
    if not isinstance(arguments, list):
        arguments = list(arguments)
    command_sys_argv: List[str] = sys.argv[:1] + arguments
    prior_current_directory: str = os.path.abspath(os.path.curdir)
    os.chdir(directory)
    try:
        if echo:
            print(
                list2cmdline([sys.executable, "-m", module_name] + arguments)
            )
        # Plugging a dummy function into `sys.exit` is necessary to avoid CLI
        # tools such as pip from ending the current process
        sys.exit = _dummy_sys_exit  # type: ignore
        sys.argv = command_sys_argv
        runpy.run_module(module_name, run_name="__main__")
    finally:
        sys.exit = prior_sys_exit  # type: ignore
        os.chdir(prior_current_directory)
        sys.argv = prior_sys_argv


def _validate_key(key: str) -> None:
    if not key.startswith("-"):
        raise ValueError(
            f'{repr(key)} is not a valid keyword. Keyword must begin with "-".'
        )


def _get_keys_set(keys: Optional[Iterable[str]] = None) -> Optional[Set[str]]:
    if keys is not None:
        if isinstance(keys, str):
            keys = {keys}
        elif not isinstance(keys, set):
            keys = set(keys)
        deque(map(_validate_key, keys), maxlen=0)
    return keys


def _iter_reversed_sys_argv_indices(
    keys: Optional[Iterable[str]] = None,
    argv: Optional[List[str]] = None,
    depth: int = 1,
) -> Iterable[int]:
    """
    In reverse order, yield the indices of the item in `sys.argv`
    index one of the indicated keys. If no `keys` are provided, yield the
    indices of all positional arguments.
    """
    if argv is None:
        argv = sys.argv
    keys = _get_keys_set(keys)
    length: int = len(argv)
    index: int
    negative_index: int
    for negative_index, value in enumerate(reversed(argv[depth:]), 1):
        index = length - negative_index
        if keys is not None:
            if value in keys:
                yield index
        elif not value.startswith("-"):
            try:
                if not argv[index - 1].startswith("-"):
                    yield index
            except IndexError:
                yield index


@overload
def iter_sys_argv_pop(
    keys: None,
    argv: Optional[List[str]],
    flag: bool,
) -> Iterable[str]:
    #
    ...


@overload
def iter_sys_argv_pop(keys: None, argv: Optional[List[str]]) -> Iterable[str]:
    #
    ...


@overload
def iter_sys_argv_pop(
    keys: None,
) -> Iterable[str]:
    #
    ...


@overload
def iter_sys_argv_pop() -> Iterable[str]:
    #
    ...


@overload
def iter_sys_argv_pop(
    keys: Optional[Iterable[str]],
    argv: Optional[List[str]],
    flag: Optional[bool],
    depth: int = 1,
) -> Iterable[Union[str, bool]]:  #
    ...


def iter_sys_argv_pop(
    keys: Optional[Iterable[str]] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
    depth: int = 1,
) -> Iterable[Union[str, bool]]:
    """
    Remove and yield all values, in reverse order, for an argument,
    from `sys.argv`.

    Parameters:

    - keys ([str]|str): Zero or more keywords/flags. If not `keys` are
      provided, this will yield positional argument values instead.
    - default (str|None) = None: If the argument is not found, this value
      is returned.
    - arg ([str]) = sys.argv: If provided, this list will be parsed instead
      of `sys.argv`.
    - flag (bool) = False: If `True`, treat the argument as a flag.
      If `False`, treat the argument as a flag only if it is not followed
      by a value.
    - depth (int) = 1: The number of items in `sys.argv` which should be
      interpreted as commands rather than positional arguments

    Examples:

    >>> deque(
    ...     map(
    ...         print,
    ...         iter_sys_argv_pop(
    ...             keys=("-r", "--requirement"),
    ...             argv=[
    ...                 "pip",
    ...                 "install",
    ...                 "-r", "requirements.txt",
    ...                 "--requirement", "dev_requirements.txt",
    ...                 "pytest",
    ...                 "tox",
    ...                 ".",
    ...             ]
    ...         )
    ...     ),
    ...     maxlen=0
    ... )
    dev_requirements.txt
    requirements.txt
    deque([], maxlen=0)

    >>> deque(
    ...     map(
    ...         print,
    ...         iter_sys_argv_pop(
    ...             argv=[
    ...                 "pip",
    ...                 "install",
    ...                 "-r", "requirements.txt",
    ...                 "--requirement", "dev_requirements.txt",
    ...                 "pytest",
    ...                 "tox",
    ...                 ".",
    ...             ],
    ...             depth=2,
    ...         )
    ...     ),
    ...     maxlen=0
    ... )
    .
    tox
    pytest
    deque([], maxlen=0)
    """
    return _iter_sys_argv_function(
        keys=keys, argv=argv, flag=flag, function=list.pop, depth=depth
    )


@overload
def iter_sys_argv_get(
    keys: None,
    argv: Optional[List[str]],
    flag: bool,
    depth: int,
) -> Iterable[str]:  #
    ...


@overload
def iter_sys_argv_get(
    keys: None, argv: Optional[List[str]], flag: Optional[bool], depth: int
) -> Iterable[str]:  #
    ...


@overload
def iter_sys_argv_get(
    keys: None,
) -> Iterable[str]:  #
    ...


@overload
def iter_sys_argv_get(
    keys: Optional[Iterable[str]],
    argv: Optional[List[str]],
    flag: Optional[bool],
    depth: int,
) -> Iterable[Union[str, bool]]:  #
    ...


def iter_sys_argv_get(
    keys: Optional[Iterable[str]] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
    depth: int = 1,
) -> Iterable[Union[str, bool]]:
    """
    Yield all values, in reverse order, for an argument, from `sys.argv`.
    If `keys` are provided, yield values for that keyword argument. If
    `keys` are *not* provided, yield positional arguments values.

    Parameters:

    - keys ([str]|str): Zero or more keywords/flags. If not `keys` are
      provided, this will yield positional argument values instead.
    - default (str|None) = None: If the argument is not found, this value
      is returned.
    - arg ([str]) = sys.argv: If provided, this list will be parsed instead
      of `sys.argv`.
    - flag (bool) = False: If `True`, treat the argument as a flag.
      If `False`, treat the argument as a flag only if it is not followed
      by a value.
    - depth (int) = 1: The number of items in `sys.argv` which should be
      interpreted as commands rather than positional arguments

    Examples:

    >>> deque(
    ...     map(
    ...         print,
    ...         iter_sys_argv_get(
    ...             keys=("-r", "--requirement"),
    ...             argv=[
    ...                 "pip",
    ...                 "install",
    ...                 "-r", "requirements.txt",
    ...                 "--requirement", "dev_requirements.txt",
    ...                 "pytest",
    ...                 "tox",
    ...                 ".",
    ...             ]
    ...         )
    ...     ),
    ...     maxlen=0
    ... )
    dev_requirements.txt
    requirements.txt
    deque([], maxlen=0)

    >>> deque(
    ...     map(
    ...         print,
    ...         iter_sys_argv_get(
    ...             argv=[
    ...                 "pip",
    ...                 "install",
    ...                 "-r", "requirements.txt",
    ...                 "--requirement", "dev_requirements.txt",
    ...                 "pytest",
    ...                 "tox",
    ...                 ".",
    ...             ],
    ...             depth=2,
    ...         )
    ...     ),
    ...     maxlen=0
    ... )
    .
    tox
    pytest
    deque([], maxlen=0)
    """
    return _iter_sys_argv_function(
        keys=keys, argv=argv, flag=flag, function=list.__getitem__, depth=depth
    )


def _iter_sys_argv_function(
    keys: Optional[Iterable[str]] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
    function: Callable[[list, int], Union[str, bool]] = list.pop,
    depth: int = 1,
) -> Iterable[Union[str, bool]]:
    if argv is None:
        argv = sys.argv
    index: Optional[int]
    for index in _iter_reversed_sys_argv_indices(
        keys=keys, argv=argv, depth=depth
    ):
        if keys is None:
            yield function(argv, index)
        else:
            value_index: int = index + 1
            # If there is no value following the keyword, it's a boolean flag
            if len(argv) <= value_index or argv[value_index].startswith("-"):
                assert flag is not False
                function(argv, index)
                yield True
            else:
                if flag:
                    value = True
                else:
                    value = function(argv, value_index)  # type: ignore
                function(argv, index)
                yield value


@overload
def sys_argv_pop(keys: None) -> Optional[str]:  #
    ...


@overload
def sys_argv_pop(
    keys: Optional[Iterable[str]] = None,
    default: Optional[str] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
) -> Union[str, bool, None]:  #
    ...


def sys_argv_pop(
    keys: Optional[Iterable[str]] = None,
    default: Optional[str] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
    depth: int = 1,
) -> Union[str, bool, None]:
    """
    Remove and return the last value for a keyword argument from `sys.argv`,
    or `None` if there are not any positional arguments.

    Parameters:

    - keys ([str]|str|None): Zero or more keywords. For example:
      `("-u", "--user")` or `"--user"`. If no `keys` are provided, the last
      positional argument will be removed and returned instead.
    - default (str|None) = None: If the argument is not found, this value
      is returned.
    - arg ([str]) = sys.argv: If provided, this list will be parsed instead
      of `sys.argv`.
    - depth (int) = 1: The number of items in `sys.argv` which should be
      interpreted as commands rather than positional arguments

    Examples:

    >>> print(sys_argv_pop(
    ...     keys=("-r", "--requirement"),
    ...     argv=[
    ...         "pip",
    ...         "install",
    ...         "-r", "requirements.txt",
    ...         "--requirement", "dev_requirements.txt",
    ...         "pytest",
    ...         "tox",
    ...         ".",
    ...     ]
    ... ))
    dev_requirements.txt

    >>> print(sys_argv_pop(
    ...     argv=[
    ...         "pip",
    ...         "install",
    ...         "-r", "requirements.txt",
    ...         "--requirement", "dev_requirements.txt",
    ...         "pytest",
    ...         "tox",
    ...         ".",
    ...     ]
    ... ))
    .
    """
    try:
        return next(
            iter(
                iter_sys_argv_pop(keys=keys, argv=argv, flag=flag, depth=depth)
            )
        )
    except StopIteration:
        return default


@overload
def sys_argv_get(keys: None) -> Optional[str]:  #
    ...


@overload
def sys_argv_get(
    keys: Optional[Iterable[str]] = None,
    default: Optional[str] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
) -> Union[str, bool, None]:  #
    ...


def sys_argv_get(
    keys: Optional[Iterable[str]] = None,
    default: Optional[str] = None,
    argv: Optional[List[str]] = None,
    flag: Optional[bool] = None,
    depth: int = 1,
) -> Union[str, bool, None]:
    """
    If `keys` are provided: Return the last value for a keyword argument from
    `sys.argv`, or `None` if the keyword argument is not present.

    If `keys` are *not* provided, return the last positional argument or
    `None` if there are no positional arguments.

    Parameters:

    - keys ([str]|str|None): Zero or more keywords. For example:
      `("-u", "--user")` or `"--user"`. If no `keys` are provided, the last
      positional argument will be removed and returned instead.
    - default (str|None) = None: If the argument is not found, this value
      is returned.
    - arg ([str]) = sys.argv: If provided, this list will be parsed instead
      of `sys.argv`.

    Examples:

    >>> print(sys_argv_get(
    ...     keys=("-r", "--requirement"),
    ...     argv=[
    ...         "pip",
    ...         "install",
    ...         "-r", "requirements.txt",
    ...         "--requirement", "dev_requirements.txt",
    ...         "pytest",
    ...         "tox",
    ...         ".",
    ...     ]
    ... ))
    dev_requirements.txt

    >>> print(sys_argv_get(
    ...     argv=[
    ...         "pip",
    ...         "install",
    ...         "-r", "requirements.txt",
    ...         "--requirement", "dev_requirements.txt",
    ...         "pytest",
    ...         "tox",
    ...         ".",
    ...     ]
    ... ))
    .
    """
    try:
        return next(
            iter(
                iter_sys_argv_get(keys=keys, argv=argv, flag=flag, depth=depth)
            )
        )
    except StopIteration:
        return default
