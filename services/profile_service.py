import httpx
from schemas.profile_schemas import AsdProfileSchema, CarerProfileSchema
from utils.http_client import request

PROFILE_SERVICE_URL = "https://backend-profile-service-1023529830652.europe-west1.run.app"

async def get_asd_profiles():
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/")

async def get_asd_profile_by_id(profile_id: str):
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}")

async def get_asd_profile_by_carer_id(carer_id: str):
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/carer/{carer_id}")

async def get_carer_profiles():
    return await request("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/")

async def get_carer_profile_by_id(carer_id: str):
    return await request("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/{carer_id}")

async def get_carer_profile_by_email(email: str):
    return await request ("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/email/{email}")

async def update_profile_for_asd(asdProfile: AsdProfileSchema, asd_id: str):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{asd_id}", json=asdProfile.dict())

async def update_asd_profile_activities_exercices(profile_id: str, exercices: list, activities: list):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}/update-education", json={
        "exercises": exercices,
        "activities": activities
    })

async def update_asd_profile_exercice_histories(profile_id: str, exercice_histories: list):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}/update-exercice-histories", json={
        "exercice_histories": exercice_histories,
    })


async def create_asd_profile(asdProfile: AsdProfileSchema, carer_id: str):
    data = asdProfile.dict()
    return await request("POST", f"{PROFILE_SERVICE_URL}/asd_profiles/{carer_id}", json=data)

async def create_carer_profile(carerProfile: CarerProfileSchema):
    data = carerProfile.dict()
    return await request("POST", f"{PROFILE_SERVICE_URL}/carer_profiles/", json=data)
