from typing import Optional
from pydantic import BaseModel


class GeneratePostRequest(BaseModel):
    length: str  # "Short", "Medium", or "Long"
    language: str  # "English" or "Hinglish"
    tag: str
    custom_input: Optional[str] = None
    model_name: str = "llama-3.3-70b-versatile"


class SimilarPostsRequest(BaseModel):
    query: str
    length: str
    language: str
    tag: str
    k: int = 3