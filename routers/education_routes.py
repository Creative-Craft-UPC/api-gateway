
from fastapi import APIRouter, HTTPException
from helpers.education_helper import activity_helper, exercice_helper
from helpers.profile_helper import asd_profile_helper
from schemas.education_schemas import ActivitySchema, ActivityResponse, ExercicesResponse, ExercicesSchema
from schemas.profile_schemas import AsdProfileResponse, AsdProfileSchema
from services.profile_service import create_asd_profile, update_asd_profile_activities_exercices
from services.education_service import create_default_activities, generate_instruction_audios, generate_listen_exercices, generate_stories_exercices, get_activity_by_id, get_exercice_by_id, update_activity, update_exercice



router = APIRouter()

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
async def update_activity_by_id(activity: ActivitySchema, activity_id: str):
    activity_dict = activity.dict()
    db_activity = await get_activity_by_id(activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    if db_activity["instructions"] != activity_dict["instructions"]:
        activity_instruction = activity_dict["instructions"]
        new_audio_url = await generate_instruction_audios([activity_instruction])
        activity_dict["audio"] = new_audio_url[0]
    else:
        activity_dict["audio"] = db_activity["audio"]
    activity_updated = await update_activity(activity_id, activity_dict)

    return await activity_helper(activity_updated)

@router.put("/exercices/{exercice_id}", response_model=ExercicesResponse)
async def update_exercice_by_id(exercice: ExercicesSchema, exercice_id: str):
    db_exercice = await get_exercice_by_id(exercice_id)
    if not db_exercice:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    exercice_updated = await update_exercice(exercice_id, exercice.dict())
    return await exercice_helper(exercice_updated)

#@router.post("/generate/exercices", response_model=list[ExercicesResponse])
#async def generate_exercices(asd_profile: AsdProfileSchema):
#    response = await generate_stories_exercices(asd_profile)
#    return response

#@router.post("/generate/exercices/audio", response_model=list[ExercicesResponse])
#async def generate_audio_exercices(asd_profile: AsdProfileSchema):
#    response = await generate_listen_exercices(asd_profile)
#    return response

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
async def get_education_activity_by_id(activity_id: str):
    response = await get_activity_by_id(activity_id)
    if not response:
        raise HTTPException(status_code=404, detail="Activity not found")
    return await activity_helper(response)

@router.get("/exercices/{exercice_id}", response_model=ExercicesResponse)
async def get_education_exercice_by_id(exercice_id: str):
    response = await get_exercice_by_id(exercice_id)
    if not response:
        raise HTTPException(status_code=404, detail="Exercice not found")
    return await exercice_helper(response)
