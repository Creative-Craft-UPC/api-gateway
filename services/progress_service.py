from schemas.ia_schema import AudioPromptSchema
from schemas.progress_schema import ExerciceHistoryDto
from utils.http_client import request


PROGRESS_SERVICE_URL = "https://backend-progress-service-1023529830652.europe-west1.run.app"

async def post_create_exercice_history(exercice_history: ExerciceHistoryDto):
    data = {
        "max_time": 0,
        "min_time" : 0, 
        "attempts" : [],
        "total_errors": 0, 
        "exercice": exercice_history.exerciceId,
    }
    return await request("POST", f"{PROGRESS_SERVICE_URL}/exercice_histories/", json=data)

async def get_exercice_histories():
    return await request("GET", f"{PROGRESS_SERVICE_URL}/exercice_histories/")

async def get_exercice_histories_by_id(history_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/exercice_histories/{history_id}")

async def post_generate_audio_realtime(audioPrompt: AudioPromptSchema):
    data = audioPrompt.dict()
    return await request("POST", f"{IA_SERVICE_URL}/api/model/audio/real-time", json=data)
