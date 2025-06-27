from schemas.ia_schema import AudioPromptSchema
from utils.http_client import request


IA_SERVICE_URL = "http://localhost:8003"

async def post_generate_exercice(prompt: str):
    return await request("POST", f"{IA_SERVICE_URL}/api/model/exercice/", json={
        "prompt": prompt
    })

async def post_generate_audio(audioPrompt: AudioPromptSchema):
    #data = audioPrompt.dict()
    return await request("POST", f"{IA_SERVICE_URL}/api/model/audio/download", json=audioPrompt)

async def post_generate_audio_realtime(audioPrompt: AudioPromptSchema):
    data = audioPrompt.dict()
    return await request("POST", f"{IA_SERVICE_URL}/api/model/audio/real-time", json=data)
