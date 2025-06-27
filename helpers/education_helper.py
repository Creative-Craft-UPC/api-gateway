async def activity_helper(activity: dict) -> dict:
    return{
        "id": str(activity["id"]),
        "instructions": activity["instructions"],
        "type": activity["type"],
        "subtype": activity.get("subtype"),
        "statement": activity["statement"],
        "audio": activity.get("audio"),

    }

async def exercice_helper(exercice: dict) -> dict:
    return{
        "id": str(exercice["id"]),
        "audio": exercice.get("audio"),
        "question": exercice.get("question"),
        "answer": exercice["answer"],
        "options": exercice.get("options", []),
        "image_options": exercice.get("image_options", []),
        "principal_image": exercice.get("principal_image"),
        "type": exercice["type"],
        "subtype": exercice.get("subtype")
    }
