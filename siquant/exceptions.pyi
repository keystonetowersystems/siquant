from typing import Any, Union, Tuple, Type

from .units import SIUnit

class UnitMismatchError(ValueError):
    def __init__(self, u1: SIUnit, u2: SIUnit) -> None: ...

class ImmutabilityError(AttributeError):
    def __init__(self, instance: Any, name: str) -> None: ...

def unexpected_type_error(
    arg_name: str, expected_type: Union[Type, Tuple[Type, ...]], actual_value: Any
) -> TypeError: ...
