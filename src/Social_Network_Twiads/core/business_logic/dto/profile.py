from dataclasses import dataclass
from datetime import date
from typing import Optional
from django.core.files import File


@dataclass
class EditProfileDto:
    avatar: File | None 
    username: str
    first_name: str
    last_name: str
    birth_date: date
    email: str
    bio: str
    country: Optional[str]
    