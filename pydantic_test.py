from pydantic_ai import Agent
from pydantic import BaseModel

class Failed(BaseModel):
    """A model representing a failed operation."""
    reason: str

