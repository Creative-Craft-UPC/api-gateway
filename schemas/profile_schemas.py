from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, StringConstraints

from schemas.education_schemas import ActivityResponse, ActivitySchema, ExercicesResponse, ExercicesSchema
from schemas.progress_schema import RecordResponse

class AsdProfileSchema(BaseModel):
    firstname: Annotated[str, StringConstraints(min_length=1, max_length=30)] = Field(..., example="Jose")
    lastname: Annotated[str, StringConstraints(min_length=1, max_length=30)] = Field(..., example="Armando")
    age: Annotated[int, Field(ge=6, le=11)] = Field(..., example=8)
    gender: Annotated[str, StringConstraints(pattern="^(masculino|femenino|otro)$")] = Field(..., example="femenino")
    severityLevel: Annotated[int, Field(ge=1, le=2)] = Field(..., example=2)
    favouriteColor: str = Field(..., example="azul")
    avatar: Optional[str] = Field(None)
    visualComprehension: Annotated[int, Field(ge=1, le=3)] = Field(..., example=2)
    emotionsKnown: List[str] = Field(default_factory=list, example=["alegría", "tristeza", "temor"])
    instructionsComprehension: Annotated[str, StringConstraints(pattern="^(bajo|medio|alto)$")] = Field(..., example="medio")
    avoidingStimuly: str = Field(..., example="Sonidos fuertes")

class AsdProfileUpdateSchema(BaseModel):
    firstname: Optional[Annotated[str, StringConstraints(min_length=1, max_length=30)]] = Field(..., example="Jose")
    lastname: Optional[Annotated[str, StringConstraints(min_length=1, max_length=30)]] = Field(..., example="Armando")
    age: Optional[Annotated[int, Field(ge=6, le=11)]] = Field(..., example=8)
    gender: Optional[Annotated[str, StringConstraints(pattern="^(masculino|femenino|otro)$")]] = Field(..., example="femenino")
    severityLevel: Optional[Annotated[int, Field(ge=1, le=2)]] = Field(..., example=2)
    favouriteColor: Optional[str] = Field(..., example="azul")
    avatar: Optional[str] = Field(None)
    visualComprehension: Optional[Annotated[int, Field(ge=1, le=3)]] = Field(..., example=2)
    emotionsKnown: Optional[List[str]] = Field(default_factory=list, example=["alegría", "tristeza", "temor"])
    instructionsComprehension: Optional[Annotated[str, StringConstraints(pattern="^(bajo|medio|alto)$")]] = Field(..., example="medio")
    avoidingStimuly: Optional[str] = Field(..., example="Sonidos fuertes")
    
class AsdProfileResponse(AsdProfileSchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    activities: List[ActivityResponse]
    exercices: List[ExercicesResponse]
    records: List[RecordResponse]

class CarerProfileSchema(BaseModel):
    firstname: Annotated[str, StringConstraints(min_length=1)] = Field(..., example="Martin")
    lastname: Annotated[str, StringConstraints(min_length=1)] = Field(..., example="Cueva")
    email: str = Field(..., example="example@example.com")
    #asd_profiles: Optional[List[str]] = Field(default_factory=list, description="Lista de IDs de perfiles de niños con TEA")

class CarerProfileResponse(BaseModel):
    id: str
    firstname: str
    lastname: str
    email: str
    asd_profiles: List[AsdProfileResponse]

class UpdateEducationforAsdProfileSchema(BaseModel):
    activities: Optional[List[str]] = Field(default_factory=list)
    exercises: Optional[List[str]] = Field(default_factory=list)

class UpdateExerciceHistoriesForAsdProfileSchema(BaseModel):
    records: Optional[List[str]] = Field(default_factory=list)

    