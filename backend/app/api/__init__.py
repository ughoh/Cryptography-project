from fastapi import APIRouter
from .api_v1 import decryption_router, encryption_router

router_v1 = APIRouter(prefix="/api/v1", tags=["api_v1"])
router_v1.include_router(decryption_router)
router_v1.include_router(encryption_router)
