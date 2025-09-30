from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, StringConstraints


class ActivityBase(BaseModel):
    type: Annotated[str, StringConstraints(
        pattern="^(Escucha emoción|Historias|Resuelve problema)"
    )] = Field(..., example="Resuelve problema")
    subtype: Optional[Annotated[str, StringConstraints(
        pattern="^(emocional|social)"
    )]] = Field(None, example="emocional")

class ActivitySchema(ActivityBase):
    instructions: Annotated[str, StringConstraints(min_length=1)] = Field(..., example="Escucha atentamente el audio, espera a que termine y selecciona la emoción que expresa.")
    statement: Annotated[str, StringConstraints(min_length=1)] = Field(None, example="Arma el rompecabezas")
    audio: Optional[str] = Field(..., example="audio_exercise_3781j3i190djd38.mp3")


class ActivityResponse(ActivitySchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")


class ExercisesSchema(ActivityBase):
    audio: Optional[str] = Field(..., example="audio_exercise_3781j3i190djd38.mp3")
    question: Optional[str] = Field(None, example="¿Cómo se siente el niño?")
    answer: str = Field(..., example="alegria")
    options: List[str] = Field(default_factory=list, example=["alegría", "tristeza", "temor"])
    image_options: List[str] = Field(default_factory=list, example=["alegría.png", "tristeza.png", "temor.png"])
    principal_image: Optional[str] = Field(None, example="main_image.png")


class ExercisesResponse(ExercisesSchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")