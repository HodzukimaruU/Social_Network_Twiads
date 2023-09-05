from typing import Any, TypeVar

from dacite import from_dict

T = TypeVar("T")


def convert_data_from_form_to_dto(dto: type[T], data_from_form: dict[str, Any]) -> Any:
    return from_dict(dto, data_from_form)
