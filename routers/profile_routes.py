from fastapi import APIRouter, HTTPException, Depends
import httpx
from auth.firebase_dep import get_current_user  # valida token Firebase
from auth.internal_token import mint_internal_token  # genera token interno

from helpers.profile_helper import asd_profile_helper, carer_profile_helper, carer_profile_light_helper
from schemas.profile_schemas import AsdProfileResponse, AsdProfileSchema, AsdProfileUpdateSchema, CarerProfileLightResponse, CarerProfileResponse, CarerProfileSchema
from services.profile_service import create_carer_profile, get_asd_profile_by_carer_id, get_asd_profile_by_id, get_carer_profile_by_email, get_carer_profile_by_id, update_profile_for_asd

router = APIRouter()

#GET carer profile by ID
@router.get("/carer_profile/{carer_id}", response_model=CarerProfileLightResponse)
async def get_profile_by_id_for_carer(carer_id: str, user=Depends(get_current_user)):
    user_id = user["uid"]
    internal_token = mint_internal_token(user_id=user_id)
    headers={"Authorization": f"Bearer {internal_token}"}
    carer_profile = await get_carer_profile_by_id(carer_id,headers=headers)
    return await carer_profile_light_helper(carer_profile)

@router.post("/carer_profile/login/{email}", response_model=CarerProfileLightResponse)
async def login_profile(email: str):
    response = await get_carer_profile_by_email(email)
    if response:
        return await carer_profile_light_helper(response)
    else:
        raise HTTPException(status_code=404, detail="Usuario no está registrado")
    
@router.patch("/asd_profile/{asd_id}", response_model=AsdProfileResponse)
async def update_asd_profile_by_id(asd_id: str, asdProfile: AsdProfileUpdateSchema, user=Depends(get_current_user)):
    user_id = user["uid"]
    internal_token = mint_internal_token(user_id=user_id)
    headers={"Authorization": f"Bearer {internal_token}"}
    response = await update_profile_for_asd(asdProfile, asd_id, headers=headers)
    if response:
        return await asd_profile_helper(response, headers)
    else:
        raise HTTPException(status_code=404, detail="Usuario no está registrado o datos incompletos")


#GET asd profiles by carer ID
@router.get("/asd_profile/carer/{carer_id}",response_model=list[AsdProfileResponse])
async def get_asd_profile_by_id_for_carer(carer_id: str, user=Depends(get_current_user)):
    user_id = user["uid"]
    internal_token = mint_internal_token(user_id=user_id)
    headers={"Authorization": f"Bearer {internal_token}"}
    
    asd_profiles = []
    profiles = await get_asd_profile_by_carer_id(carer_id, headers=headers)
    if not profiles:
        return []
    for asd_profile in profiles:
        asd_profiles.append(await asd_profile_helper(asd_profile, headers))
    return asd_profiles

#POST new carer profile
@router.post("/carer_profile", response_model = CarerProfileLightResponse)
async def create_profile_for_carer(profile: CarerProfileSchema):
    created_carer_profile = await create_carer_profile(profile)
    if not created_carer_profile:
        raise HTTPException(status_code=500, detail="Error del servicio de perfil")
    return created_carer_profile 

#GET asd profile by ID
@router.get("/asd_profile/{asd_id}", response_model=AsdProfileResponse)
async def get_profile_by_id_for_asd(asd_id: str, user=Depends(get_current_user)):
    user_id = user["uid"]
    internal_token = mint_internal_token(user_id=user_id)
    headers={"Authorization": f"Bearer {internal_token}"}
    
    asd_profile = await get_asd_profile_by_id(asd_id, headers=headers)
    return await asd_profile_helper(asd_profile, headers)
