async def activity_helper(activity: dict) -> dict:
    return{
        "id": str(activity["id"]),
        "instructions": activity["instructions"],
        "type": activity["type"],
        "subtype": activity.get("subtype"),
        "statement": activity["statement"],
        "audio": activity.get("audio"),

    }

async def exercise_helper(exercise: dict) -> dict:
    return{
        "id": str(exercise["id"]),
        "audio": exercise.get("audio"),
        "question": exercise.get("question"),
        "answer": exercise["answer"],
        "options": exercise.get("options", []),
        "image_options": exercise.get("image_options", []),
        "principal_image": exercise.get("principal_image"),
        "type": exercise["type"],
        "subtype": exercise.get("subtype")
    }
