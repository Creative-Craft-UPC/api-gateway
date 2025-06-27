from typing import Optional
from pydantic import BaseModel, Field, StringConstraints

class AudioPromptSchema(BaseModel):
    text: str = Field(..., example="¡Fui al parque, jugué mucho y me divertí!")
    voice: str = Field(default="nova", example="nova")
    audio_name: Optional[str] = Field(..., example="audio-alegría-9fdisa-38d8s9f8-s9a9f78s")
    instructions: str = Field(..., example="Lee el texto con una voz animada, brillante y rápida. Usa entonación ascendente y énfasis positivo")