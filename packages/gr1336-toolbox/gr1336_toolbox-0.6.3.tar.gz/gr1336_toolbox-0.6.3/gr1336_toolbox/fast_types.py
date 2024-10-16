from pathlib import Path
from typing import Any, Literal, Union, TypeGuard


def is_float(entry: Any, check_string: bool = False) -> TypeGuard[float]:
    """
    Checks if the entry provided is a valid float. It can check if a string can be converted to float if check_string is True.

    Args:
        entry (Any): The value to be checked.
        check_string (bool, optional): If True, it will check if the value can be converted to float.

    Returns:
        bool: If True, means that is a valid float otherwise false.
    """
    if isinstance(entry, float):
        return True
    if not check_string or not is_string(entry, False, True):
        return False
    try:
        entry = str(entry)
        float(entry)
        return True
    except:
        return False


def is_int(entry: Any, check_string: bool = False) -> TypeGuard[int]:
    """Checks if a number is a valid integer.

    Args:
        entry (Any): The item to be check if is a valid integer
        check_string (bool, optional): To check strings to see if its a possible number. Defaults to False.

    Returns:
        bool: True if its a True integer otherwise False.
    """
    if isinstance(entry, int):
        return True
    if not check_string or not is_string(entry, False, True):
        return False
    return str(entry).isdigit()


def is_dict(entry: Any, allow_empty: bool = False) -> TypeGuard[dict]:
    """Check if the provided entry is a valid dictionary and if it has content or not (if allow_empty is False).

    Args:
        entry (Any): The value to be checked if its True.
        allow_empty (bool, optional): If True it allow empty dictionaries to be evaluated, otherwise it requires it to be a dictionary and have at least some content there. Defaults to False.

    Returns:
        bool: True if valid dictionary and (if allow_empty is False) if it has some content in it.
    """
    return isinstance(entry, dict) and (allow_empty or bool(entry))


def keys_in_text(
    sources: str,
    has_any: str | list[str],
    force_lower_case: bool = False,
):
    """Basically the reverse of **in** function, it can be used to locate if **sources** contains anything from the **has_any** into it.

    Args:
        sources (str):
            Target string to be checked if has any of the provided keys.
        has_any (str | list[str]):
            The string or list of strings to be checked if they are or not in the text.
            If its a string each letter will be checked, if its a list of string, then each word in the list will be checked instead.
        force_lower_case (bool, optional):
            If true will set everything to lower-case (both source and has_any).
            This is useful for tasks that dont require a case-sensitive scan. Defaults to False.

    Returns:
        bool: If any key was found will be returned as true, otherwise False.
    """
    if not is_string(sources) or (not is_string(has_any) and not is_array(has_any)):
        return False

    if is_array(has_any):
        has_any = [
            x.lower() if force_lower_case else x for x in has_any if is_string(x)
        ]
        assert has_any, "has_any had no valid string!"

    if force_lower_case:
        sources = sources.lower()
        if is_string(has_any):
            has_any = has_any.lower()  # type: ignore

    for elem in has_any:
        if elem in sources:
            return True
    return False


def is_number(entry: Any, check_string: bool = False) -> TypeGuard[Union[int, float]]:
    """Check if the entry is a number (being either a int or float). It also check if in case its a string (and check_string is True) if its a valid number if converted.

    Args:
        entry (Any): The entry to be checked.
        check_string (bool, optional): If True will check if entry can be converted to float, case the entry is a string. Defaults to False.

    Returns:
        bool: True if the entry is either a float or a integer, otherwise False.

    Examples:
        if for example 'entry' is a string and check_string is set to True:
        ```python
        a = "1"
        b = "text"
        c = "1.56"
        print(is_number(a, check_string=True)) # True
        print(is_number(a, check_string=False)) # False
        print(is_number(b, check_string=True)) # False
        print(is_number(b, check_string=False)) # False
        print(is_number(c, check_string=True)) # True
        print(is_number(c, check_string=False)) # False
        float(a) # ok
        float(b) # ValueError
        float(c) # ok
        ```

    """
    return is_int(entry, check_string) or is_float(entry, check_string)


def is_string(
    entry: Any,
    allow_empty: bool = False,
    strip_string: bool = False,
) -> TypeGuard[str]:
    """Check if an entry is a string, bytes or a Path object.

    if ``strip_string`` is set to True, then the entry will be striped will be stripped before the final checking (Its useless when allow empty is False).
    """
    if not isinstance(entry, (str, bytes)):
        return False
    if not allow_empty and strip_string:
        entry = entry.strip()
    return allow_empty or bool(entry)


def is_list(entry: Any, allow_empty: bool = False) -> TypeGuard[list]:
    """Check if the provided entry is a list and if its not empty.

    Args:
        entry (Any): _description_
        allow_empty (bool, optional): If true, will return True if the item is a list, regardless if its empty or not. Defaults to False.

    Returns:
        bool: True if the entry is a list and if either the allow_empty is true or the list is not empty.
    """
    return isinstance(entry, list) and (allow_empty or bool(entry))


def is_tuple(entry: Any, allow_empty: bool = False) -> TypeGuard[tuple]:
    """Check if the provided entry is a valid dictionary and if it has content or not (if allow_empty is False).

    Args:
        entry (Any): The value to be checked if its True.
        allow_empty (bool, optional): If True it allow empty dictionaries to be evaluated, otherwise it requires it to be a dictionary and have at least some content there. Defaults to False.

    Returns:
        bool: True if valid dictionary and (if allow_empty is False) if it has some content in it.
    """
    return isinstance(entry, tuple) and (allow_empty or bool(entry))


def is_array(
    entry: Any, allow_empty: bool = False, **kwargs
) -> TypeGuard[Union[list, tuple]]:
    """Checks if the entry is either a list, tuple. It can also check for dictionaries if ``check_dict`` is True. Checks if its empty if allow_empty is False.

    Args:
        entry (Any): Value to be analyzed.
        allow_empty (bool, optional): If True will allow empty arrays to be returned as True. Defaults to False.
    Returns:
        bool: If True the value is a valid (non-empty if allow_empty is False else it returns true just for being a list or tuple).
    """
    if isinstance(entry, (list, tuple)):
        return allow_empty or bool(entry)
    return False


def is_boolean(entry: Any, allow_number: bool = False) -> TypeGuard[bool]:
    if not allow_number or isinstance(entry, bool):
        return isinstance(entry, bool)
    return is_int(entry) and entry in [0, 1]


def compare_none(arg1: Any | None, arg2: Any) -> Any:
    """
    arg1 if its not None or arg2.

    Useful to allow a different approach than 'or' operator in strings, for example:

    Consider that the arguments as:
    ```py
    arg1 = 0
    arg2 = 3
    ```
    If using or operator directly the following would happen:

    ```python
    results = arg1 or arg2
    # results = arg2 (3)
    ```
    It checks for Falsely data in the first item, but sometimes that value would be valid even if falsely like: `0`, `""`, `[]`, `{}`, `()` and `False`.

    So, it was made to check if the first value is None or non-None if None it uses the arg2, otherwise it returns the arg1 even if falsely.

    example:
    ```
    from gr1336_toolbox import compare_none

    results = compare_none(arg1, arg2)
    # results = arg1 (0)
    ```

    """
    return arg1 if arg1 is not None else arg2


# Not cached, path can be changed any time
def valid_path(
    entry: str | Path,
    expected_dir: Literal["file", "path", "any"] = "any",
) -> bool:
    """Checks if `entry` is a valid existent path."""
    if not isinstance(entry, (str, bytes, Path)) or not Path(entry).exists():
        return False
    entry = Path(entry)
    if expected_dir == "any":
        return True
    elif expected_dir == "file":
        return entry.is_file()
    return entry.is_dir()


def non_empty_check(value: Any, falsely: bool = False):
    """Checks if a value is not empty (must be one of the default python ones, otherwise it will not work). If its not empty returns true otherwise returns false.

    It also can check for falsely values, in strings, booleans and numbers. (If the string is only empty spaces (if text striped is empty) returns false, if boolean is false returns false, if number is zero (both int or float) it returns false).
    """
    if is_number(value):
        return True if not falsely else bool(value)
    if is_boolean(value):
        return True if not falsely else bool(value)
    if is_string(value, allow_empty=False, strip_string=falsely):
        return True
    if is_array(value):
        return True
    if is_dict(value):
        return True
    return False


__all__ = [
    "is_int",
    "is_string",
    "is_dict",
    "is_float",
    "is_number",
    "is_tuple",
    "is_list",
    "is_boolean",
    "is_array",
    "keys_in_text",
    "compare_none",
    "valid_path",
    "non_empty_check",
]
