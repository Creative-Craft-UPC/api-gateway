from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class AttemptSchema(BaseModel):
    time: float
    errors_quantity: int
    date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class AttemptDto(BaseModel):
    time: float
    errors_quantity: int


class AttemptResponse(AttemptSchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")

class ExerciceHistorySchema(BaseModel):
    max_time: float
    min_time: float
    attempts: Optional[List[str]] = Field(default_factory=list, example=["665f1b0c543ed91f9a1d0ef9","665f1b0c543ed91f9a1d0ef9"])
    total_errors: int
    exercice: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")

class ExerciceHistoryDto(BaseModel):
    exerciceId: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")

class ProgressDto(BaseModel):
    exerciceId: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    time: float
    errors_quantity: int

class ExerciceHistoryResponse(BaseModel):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    max_time: float
    min_time: float
    attempts: List[AttemptSchema]
    total_errors: int
    exercice: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    