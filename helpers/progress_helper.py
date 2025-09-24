from typing import List

from bson import ObjectId

def attempt_helper(attempt: dict) -> dict:
    return {
        "id": str(attempt["_id"]),
        "time": attempt["time"],
        "errors_quantity": attempt["errors_quantity"],
    }

async def exercice_history_helper(exercice_history: dict, attempt_collection) -> dict:
    attempts: List[dict] = []
    for attempt_id in exercice_history.get("attempts", []):
        attempt_doc = await attempt_collection.find_one({"_id": ObjectId(attempt_id)})
        if attempt_doc:
            attempts.append(attempt_helper(attempt_doc))

    return {
        "id": str(exercice_history["_id"]),
        "max_time": exercice_history["max_time"],
        "min_time": exercice_history["min_time"],
        "attempts": attempts,
        "total_errors": exercice_history["total_errors"],
        "exercice": exercice_history.get("exercice")

    }



