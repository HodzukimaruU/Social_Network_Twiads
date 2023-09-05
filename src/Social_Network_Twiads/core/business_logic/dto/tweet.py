from dataclasses import dataclass
from core.models import User, Tweet 
from typing import Optional


@dataclass
class AddTweetDTO:
    content : str
    tags : str
    author : Optional['User'] 
    parent_tweet : Tweet | None


@dataclass
class EditTweetDTO:
    content : str
    tags : str
