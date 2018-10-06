"""

"""


class UnitMismatchError(ValueError):
    def __init__(self, u1, u2):
        super().__init__("Unit Mismatch: %s, %s" % (u1, u2), u1, u2)


class ImmutabilityError(AttributeError):
    def __init__(self, instance, name):
        super().__init__(
            "Can't mutate attribute '{name}'.".format(name=name), instance, name
        )


def unexpected_type_error(arg_name, expected_type, actual_value):
    return TypeError(
        "'{name}' must be {type!r} (got {value!r} that is a "
        "{actual!r}).".format(
            name=arg_name,
            type=expected_type,
            actual=actual_value.__class__,
            value=actual_value,
        ),
        arg_name,
        expected_type,
        actual_value,
    )
