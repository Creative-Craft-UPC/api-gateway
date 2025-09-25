from typing import List

from bson import ObjectId

from services.progress_service import get_attempts_by_history_id

def attempt_helper(attempt: dict) -> dict:
    return {
        "id": str(attempt["_id"]),
        "time": attempt["time"],
        "errors_quantity": attempt["errors_quantity"],
    }

async def exercice_history_helper(exercice_history: dict) -> dict:
    attempts: List[dict] = []
    attempts = get_attempts_by_history_id(str(exercice_history["_id"]))

    return {
        "id": str(exercice_history["_id"]),
        "max_time": exercice_history["max_time"],
        "min_time": exercice_history["min_time"],
        "attempts": attempts,
        "total_errors": exercice_history["total_errors"],
        "exercice": exercice_history.get("exercice")

    }



