"""
Controlador para predicciones del modelo ML
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models.schemas import PredictionRequest, PredictionResponse, MetricsResponse
from ..services.ml_service import ml_service

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Realizar predicción",
    description="Clasifica un texto científico utilizando el modelo SciBERT entrenado"
)
async def predict_text(request: PredictionRequest) -> PredictionResponse:
    """
    Realiza una predicción sobre un texto científico.
    
    - **text**: Texto científico para clasificar (mínimo 10 caracteres, máximo 5000) (title + abstract)
    
    Retorna la clase predicha, confianza, probabilidades por categoría y categorías individuales.
    """
    try:
        if not ml_service.is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        prediction = ml_service.predict(request.text)
        return prediction
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en predicción: {str(e)}"
        )

@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="Obtener métricas del modelo",
    description="Retorna las métricas de rendimiento del modelo (F1-score, Accuracy, etc.)"
)
async def get_model_metrics() -> MetricsResponse:
    """
    Obtiene las métricas de rendimiento del modelo.
    
    Retorna F1-score, accuracy, precision, recall y número total de clases.
    """
    try:
        metrics = ml_service.get_model_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo métricas: {str(e)}"
        )

@router.get(
    "/classes",
    response_model=List[str],
    summary="Obtener clases disponibles",
    description="Retorna la lista de todas las clases que puede predecir el modelo"
)
async def get_available_classes() -> List[str]:
    """
    Obtiene las clases disponibles del modelo.
    
    Retorna una lista con todas las clases que puede predecir el modelo.
    """
    try:
        if not ml_service.is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        classes = ml_service.get_available_classes()
        return classes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo clases: {str(e)}"
        )
