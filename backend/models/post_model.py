from typing import List, Optional
from pydantic import BaseModel


class Post(BaseModel):
    text: str
    engagement: int = 0
    line_count: int
    language: str
    tags: List[str]

    def categorize_length(self) -> str:
        if self.line_count <= 5:
            return "Short"
        elif 6 <= self.line_count <= 10:
            return "Medium"
        else:
            return "Long"