import httpx
from schemas.profile_schemas import AsdProfileSchema, CarerProfileSchema
from utils.http_client import request

PROFILE_SERVICE_URL = "http://127.0.0.1:8003"
#PROFILE_SERVICE_URL = "https://backend-profile-service-31496243302.europe-west1.run.app"

async def get_asd_profiles(headers: dict):
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/",headers=headers)

async def get_asd_profile_by_id(profile_id: str, headers: dict):
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}",headers=headers)

async def get_asd_profile_by_carer_id(carer_id: str, headers: dict):
    return await request("GET", f"{PROFILE_SERVICE_URL}/asd_profiles/carer/{carer_id}",headers=headers)

async def get_carer_profiles(headers: dict):
    return await request("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/",headers=headers)

async def get_carer_profile_by_id(carer_id: str, headers: dict):
    return await request("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/{carer_id}",headers=headers)

async def get_carer_profile_by_email(email: str):
    return await request ("GET", f"{PROFILE_SERVICE_URL}/carer_profiles/email/{email}")

async def update_profile_for_asd(asdProfile: AsdProfileSchema, asd_id: str, headers: dict):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{asd_id}", json=asdProfile.dict(),headers=headers)

async def update_asd_profile_activities_exercises(profile_id: str, exercises: list, activities: list, headers: dict):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}/update-education", json={
        "exercises": exercises,
        "activities": activities
    },headers=headers)

async def update_asd_profile_records_service(profile_id: str, records: list, headers: dict):
    return await request("PATCH", f"{PROFILE_SERVICE_URL}/asd_profiles/{profile_id}/update-records", json={
        "records": records,
    },headers=headers)


async def create_asd_profile(asdProfile: AsdProfileSchema, carer_id: str, headers: dict):
    data = asdProfile.dict()
    return await request("POST", f"{PROFILE_SERVICE_URL}/asd_profiles/{carer_id}", json=data,headers=headers)

async def create_carer_profile(carerProfile: CarerProfileSchema):
    data = carerProfile.dict()
    return await request("POST", f"{PROFILE_SERVICE_URL}/carer_profiles/", json=data)
