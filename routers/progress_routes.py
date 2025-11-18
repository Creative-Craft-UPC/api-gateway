
from fastapi import APIRouter, Depends, HTTPException

from auth.firebase_dep import get_current_user
from auth.internal_token import mint_internal_token
from helpers.progress_helper import record_helper
from schemas.progress_schema import RecordResponse
from services.progress_service import get_record_by_id


router = APIRouter()

@router.get("/records/{record_id}", response_model=RecordResponse)
async def get_record_data_by_id(record_id: str, user=Depends(get_current_user)):
    user_id = user["uid"]
    internal_token = mint_internal_token(user_id=user_id)
    headers={"Authorization": f"Bearer {internal_token}"}
    record = await get_record_by_id(record_id, headers=headers)
    print(record)
    if not record:
        HTTPException(status_code=404, detail="Registro no encontrado")
    return await record_helper(record)