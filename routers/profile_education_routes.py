from fastapi import APIRouter, HTTPException
from helpers.profile_helper import asd_profile_helper
from schemas.profile_schemas import AsdProfileResponse, AsdProfileSchema
from schemas.progress_schema import AttemptDto, ProgressDto, RecordDto, RecordResponse
from services.profile_service import create_asd_profile, get_asd_profile_by_id, update_asd_profile_activities_exercices, update_asd_profile_records_service
from services.progress_service import get_records_by_user_id, post_create_record
from services.education_service import create_default_activities, create_initial_exercises
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


@router.put("/asd_profiles/{asd_id}/generate_all_exercices", response_model=AsdProfileResponse)
async def attach_education(asd_id: str):
    asd_profile = await get_asd_profile_by_id(asd_id)
    if not asd_profile:
        raise HTTPException(status_code=404, detail=f"User {asd_id} not found")
    
    new_exercices = await create_initial_exercises(asd_profile)
    exercice_ids = [exercice["id"] for exercice in new_exercices]

    updated_profile = await update_asd_profile_activities_exercices(
        asd_profile["id"], exercices=exercice_ids, activities=asd_profile.get("activities", [])
    )
    return await asd_profile_helper(updated_profile)

@router.get("/asd_profiles/{asd_id}/get_records", response_model=list[RecordResponse])
async def get_all_records_by_asd_asd_id(asd_id: str):
    records = await get_records_by_user_id(asd_id)
    return records

@router.put("/asd_profiles/{asd_id}/add_record", response_model=AsdProfileResponse)
async def update_asd_profile_records(asd_id: str, data: ProgressDto):
    asd_profile = await get_asd_profile_by_id(asd_id)
    record_id_list = []
    records = await get_records_by_user_id(asd_id)
    asd_profile_updated = asd_profile
    if len(records) > 0:
        record_id_list = asd_profile.get("records", [])
        found = next((e for e in records if e["exercise_id"] == data.exercise_id), None)
        if found:
            attempt_dto = AttemptDto(time= data.time, errors_quantity= data.errors_quantity)
            attempt = await post_create_attempt(attempt_dto, found["id"])
        else:
            record_dto = RecordDto(
                exercise_id= data.exercise_id
            )
            new_record = await post_create_record(record_dto)
            record_id_list.append(str(new_record["id"]))
            attempt_dto = AttemptDto(
                time=data.time,
                errors_quantity=data.errors_quantity
            )
            new_attempt = await post_create_attempt(attempt_dto, str(new_record["id"]))
            asd_profile_updated = await update_asd_profile_records_service(asd_id, record_id_list)

    else:
        record_dto = RecordDto(
            exercise_id= data.exercise_id
        )
        new_record = await post_create_record(record_dto)
        
        record_id_list.append(str(new_record["id"]))
        attempt_dto = AttemptDto(
            time=data.time,
            errors_quantity=data.errors_quantity
        )
        new_attempt = await post_create_attempt(attempt_dto, str(new_record["id"]))
        asd_profile_updated = await update_asd_profile_records_service(asd_id, record_id_list)


    return await asd_profile_helper(asd_profile_updated)
    
            

        



    
