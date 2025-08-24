"""
Controlador para health checks y status de la API
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from ..models.schemas import HealthResponse
from ..services.ml_service import ml_service
from ..core.config import config

router = APIRouter(tags=["System"])

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica el estado de la API y del modelo"
)
async def health_check() -> HealthResponse:
    """
    Verifica el estado de salud de la API.
    
    Retorna el estado del servicio, si el modelo está cargado, timestamp y versión.
    """
    try:
        is_model_loaded = ml_service.is_model_loaded()
        
        return HealthResponse(
            status="healthy" if is_model_loaded else "degraded",
            model_loaded=is_model_loaded,
            timestamp=datetime.now().isoformat(),
            version=config.APP_VERSION
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error en health check: {str(e)}"
        )

@router.get(
    "/info",
    summary="Información de la API",
    description="Obtiene información general sobre la API"
)
async def get_api_info():
    """
    Obtiene información general de la API.
    
    Retorna información sobre la aplicación, versión, modelo y configuración.
    """
    try:
        return {
            "app_name": config.APP_NAME,
            "version": config.APP_VERSION,
            "api_version": config.API_VERSION,
            "model_loaded": ml_service.is_model_loaded(),
            "total_classes": len(ml_service.get_available_classes()) if ml_service.is_model_loaded() else 0,
            "max_text_length": config.MAX_TEXT_LENGTH,
            "cuda_available": config.is_cuda_available(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo información: {str(e)}"
        )
