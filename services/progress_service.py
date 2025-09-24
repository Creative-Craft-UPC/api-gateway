from schemas.ia_schema import AudioPromptSchema
from schemas.progress_schema import AttemptDto, ExerciceHistoryDto, ExerciceHistorySchema
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

async def post_create_attempt(attempt: AttemptDto):
    data = attempt.dict()
    return await request("POST", f"{PROGRESS_SERVICE_URL}/attempts", json=data)

async def get_exercice_histories():
    return await request("GET", f"{PROGRESS_SERVICE_URL}/exercice_histories/")

async def get_exercice_history_by_id(history_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/exercice_histories/{history_id}")

async def get_exercice_histories_by_user_id(history_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/exercice_histories/{history_id}")

async def get_attempts_by_history_id(history_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/attempt/{history_id}")

async def patch_attempt(history_id: str, history: ExerciceHistorySchema):
    data = history.dict()
    return await request("PATCH", f"{PROGRESS_SERVICE_URL}/exercice_histories/{history_id}")


async def delete_attempt(attempt_id: str):
    return await request("DELETE", f"{PROGRESS_SERVICE_URL}/attempts/{attempt_id}")

async def delete_exercice_history(history_id: str):
    return await request("DELETE", f"{PROGRESS_SERVICE_URL}/exercice_histories/{history_id}")
