from django.core.exceptions import ValidationError
from django.core.files import File

from datetime import date


class ValidateMaxTagCount:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_tags = len(value.split("\r\n"))

        if number_of_tags > self._max_count:
            raise ValidationError(message=f"Max number of tags is {self._max_count}")
        else:
            return None


class MinAgeValidator:
    def __init__(self, min_age: int) -> None:
        self.min_age = min_age

    def __call__(self, value: date) -> None:
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < self.min_age:
            raise ValidationError(f"You must be at least {self.min_age} years old.")


class ValidateFileExtension:
    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        split_file_name = value.name.split(".")
        if len(split_file_name) < 2:
            raise ValidationError(message=f"Accept only {self._available_extensions}")

        file_extension = split_file_name[-1]

        if file_extension not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}")


class ValidateFileSize:
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(message=f"Max file size is {max_size_in_mb} MB")
