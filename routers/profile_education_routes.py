from fastapi import APIRouter, HTTPException
from helpers.profile_helper import asd_profile_helper
from schemas.profile_schemas import AsdProfileResponse, AsdProfileSchema
from schemas.progress_schema import ProgressDto
from services.profile_service import create_asd_profile, get_asd_profile_by_id, update_asd_profile_activities_exercices
from services.progress_service import get_exercice_histories_by_user_id
from services.education_service import create_default_activities, create_initial_exercises, get_activity_by_id, get_exercice_by_id
from services.progress_service import post_create_attempt

router = APIRouter()

@router.post("/asd_profiles/{carer_id}", response_model=AsdProfileResponse)
async def create_profile_for_asd(profile: AsdProfileSchema, carer_id: str):
    #Crear el perfil en ProfileService
    created_asd_profile = await create_asd_profile(profile, carer_id)

    #Crear actividades por defecto y guardarlas en bd
    default_activities = await create_default_activities()

    #Crear los ejercicios iniciales y guardarlos en bd
    initial_exercices = await create_initial_exercises(created_asd_profile)

    #Extraer los IDs de las actividades creadas
    activity_ids = [activity["id"] for activity in default_activities]

    #Extraer los IDs de los ejercicios creados
    exercice_ids = [exercice["id"] for exercice in initial_exercices]

    #Asignar al perfil creado
    updated_profile = await update_asd_profile_activities_exercices(
        created_asd_profile["id"], exercices=exercice_ids, activities=activity_ids
    )

    return await asd_profile_helper(updated_profile)


@router.put("/asd_profiles/{profile_id}/generate_all_exercices", response_model=AsdProfileResponse)
async def attach_education(profile_id: str):
    asd_profile = await get_asd_profile_by_id(profile_id)
    if not asd_profile:
        raise HTTPException(status_code=404, detail=f"User {profile_id} not found")
    
    new_exercices = await create_initial_exercises(asd_profile)
    exercice_ids = [exercice["id"] for exercice in new_exercices]

    updated_profile = await update_asd_profile_activities_exercices(
        asd_profile["id"], exercices=exercice_ids, activities=asd_profile.get("activities", [])
    )
    return await asd_profile_helper(updated_profile)

@router.put("/asd_profiles/{profile_id}/add_exercice_history", response_model=AsdProfileResponse)
async def update_asd_profile_exercice_history(profile_id: str, exercice_history: ProgressDto):
    asd_profile = await get_asd_profile_by_id(profile_id)
    if not asd_profile:
        raise HTTPException(status_code=404, detail=f"User {profile_id} not found")
    
    exercice_histories = await get_exercice_histories_by_user_id(profile_id)
    if exercice_histories:
        attemptDto = {"time": exercice_history.time, "errors_quantity": exercice_history.errors_quantity}
        attempt = await post_create_attempt(attemptDto)
        exercice_histories.append(attempt)
        
        



    
