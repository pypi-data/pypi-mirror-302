import typing as t
from ..com import ComObject, Instance
from ..errors import TaskSchdError


class BitwiseField(t.Generic[Instance]):
    _com_field: str
    _bitwise_const: int

    def __init__(self, field: str, const: int):
        self._com_field = field
        self._bitwise_const = const

    def __get__(self, instance: ComObject, owner: t.Type[Instance]) -> bool:
        return bool(getattr(instance.com_object, self._com_field) & self._bitwise_const)

    def __set__(self, obj: ComObject, value: bool):
        if not isinstance(value, bool):
            raise TaskSchdError("Value must be boolean type.")

        current = getattr(obj.com_object, self._com_field)
        print(f"current {self._com_field}: {current} | {self._bitwise_const}")
        if value is True:
            setattr(obj.com_object, self._com_field, current | self._bitwise_const)
        else:
            setattr(obj.com_object, self._com_field, current ^ self._bitwise_const)
