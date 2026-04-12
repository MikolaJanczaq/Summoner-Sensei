from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def get_server_health():
    return {"health": "ok"}