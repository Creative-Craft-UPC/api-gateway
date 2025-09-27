
from fastapi import APIRouter, HTTPException

from helpers.progress_helper import record_helper
from schemas.progress_schema import RecordResponse
from services.progress_service import get_record_by_id


router = APIRouter()

@router.get("/records/{record_id}", response_model=RecordResponse)
async def get_record_data_by_id(record_id: str):
    record = await get_record_by_id(record_id)
    print(record)
    if not record:
        HTTPException(status_code=404, detail="Registro no encontrado")
    return await record_helper(record)