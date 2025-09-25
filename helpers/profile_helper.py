
from typing import List

from services.education_service import get_activity_by_id, get_exercice_by_id
from services.profile_service import get_asd_profile_by_id
from services.progress_service import get_exercice_history_by_id

async def asd_profile_helper(asdProfile: dict) -> dict:
    activities: List[dict] = []
    for activity_id in asdProfile.get("activities",[]):
        activity = await get_activity_by_id(activity_id)
        if activity:
            activities.append(activity)

    exercices: List[dict] = []
    for exercice_id in asdProfile.get("exercices", []):
        exercice = await get_exercice_by_id(exercice_id)
        if exercice:
            exercices.append(exercice)

    exercice_histories: List[dict] = []
    for exercice_history_id in asdProfile.get("exercice_histories", []):
        exercice_history = await get_exercice_history_by_id(exercice_history_id)
        if exercice_history:
            exercice_histories.append(exercice_history)

    return {
        "id": str(asdProfile["id"]),
        "firstname": asdProfile["firstname"],
        "lastname": asdProfile["lastname"],
        "age": asdProfile["age"],
        "gender": asdProfile["gender"],
        "severityLevel": asdProfile["severityLevel"],
        "favouriteColor": asdProfile["favouriteColor"],
        "avatar": asdProfile.get("avatar"),
        "visualComprehension": asdProfile["visualComprehension"],
        "emotionsKnown": asdProfile.get("emotionsKnown", []),
        "instructionsComprehension": asdProfile["instructionsComprehension"],
        "avoidingStimuly": asdProfile["avoidingStimuly"],
        "activities": activities,
        "exercices": exercices,
        "exercice_histories": exercice_histories,
    } 


async def carer_profile_helper(carerProfile: dict) -> dict:
    asd_profiles: List[dict] = []
    for asd_profile in carerProfile.get("asd_profiles", []):
        profile_doc = await get_asd_profile_by_id(str(asd_profile["id"]))
        if profile_doc:
            asd_profiles.append(await asd_profile_helper(profile_doc))

    return {
        "id": str(carerProfile["id"]),
        "firstname": carerProfile["firstname"],
        "lastname": carerProfile["lastname"],
        "email": carerProfile["email"],
        "asd_profiles": asd_profiles
    } 



