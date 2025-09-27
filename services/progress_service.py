from schemas.ia_schema import AudioPromptSchema
from schemas.progress_schema import AttemptDto, RecordDto, RecordSchema
from services.profile_service import get_asd_profile_by_id
from utils.http_client import request


PROGRESS_SERVICE_URL = "https://backend-progress-service-1023529830652.europe-west1.run.app"

async def post_create_record(record: RecordDto):
    data = {
        "max_time": 0,
        "min_time" : 0, 
        "attempts" : [],
        "total_errors": 0, 
        "exercice_id": record.exercice_id,
    }
    return await request("POST", f"{PROGRESS_SERVICE_URL}/records/", json=data)

async def post_create_attempt(attempt: AttemptDto, record_id):
    data = attempt.dict()
    return await request("POST", f"{PROGRESS_SERVICE_URL}/attempts/{record_id}", json=data)

async def get_records():
    return await request("GET", f"{PROGRESS_SERVICE_URL}/records/")

async def get_record_by_id(record_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/records/{record_id}")

async def get_attempts_by_record_id(record_id: str):
    return await request("GET", f"{PROGRESS_SERVICE_URL}/attempts/{record_id}")

async def patch_attempt(record_id: str, history: RecordSchema):
    data = history.dict()
    return await request("PATCH", f"{PROGRESS_SERVICE_URL}/records/{record_id}", json=data)


async def delete_attempt(attempt_id: str):
    return await request("DELETE", f"{PROGRESS_SERVICE_URL}/attempts/{attempt_id}")

async def delete_record(record_id: str):
    return await request("DELETE", f"{PROGRESS_SERVICE_URL}/records/{record_id}")


async def get_records_by_user_id(profile_id: str):
    asd_data = await get_asd_profile_by_id(profile_id)
    records = []
    records_id = asd_data.get("records", [])
    if records_id:
        for id in records_id:
            record = await get_record_by_id(id)
            if record:
                records.append(record)
    return records
        
        