from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RegistrationDTO:
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    birth_date: date
    country: Optional[str]

    def __str__(self) -> str:
        return f"username={self.username} email={self.email}"
