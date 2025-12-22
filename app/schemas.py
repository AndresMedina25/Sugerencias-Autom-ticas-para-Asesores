from pydantic import BaseModel, Field

class KnowledgeItem(BaseModel):
    question: str = Field(..., min_length=3)
    answer: str = Field(..., min_length=3)