from typing import List

from bson import ObjectId

from services.progress_service import get_attempts_by_record_id

def attempt_helper(attempt: dict) -> dict:
    return {
        "id": str(attempt["id"]),
        "time": attempt["time"],
        "errors_quantity": attempt["errors_quantity"],
        "date": attempt["date"],
    }

async def record_helper(record: dict) -> dict:
    attempts: List[dict] = []
    attempts = await get_attempts_by_record_id(str(record["id"]))

    return {
        "id": str(record["id"]),
        "max_time": record["max_time"],
        "min_time": record["min_time"],
        "attempts": attempts,
        "total_errors": record["total_errors"],
        "exercise_id": record.get("exercise_id")

    }



