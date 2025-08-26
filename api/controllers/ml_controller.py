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
    summary="Realizar predicción multilabel",
    description="Clasifica un texto científico médico utilizando el modelo SciBERT entrenado con soporte multilabel"
)
async def predict_text(request: PredictionRequest) -> PredictionResponse:
    """
    Realiza una predicción multilabel sobre un texto científico médico.
    
    - **text**: Texto científico completo obtenido de la concatenación del título (title) 
      y el resumen (abstract) del artículo científico. Debe contener entre 10 y 5000 caracteres.
      Formato esperado: "{title} {abstract}"
    - **threshold**: Umbral de confianza para clasificación multilabel (valor entre 0.0 y 1.0, default: 0.5)
    
    **Categorías médicas disponibles:**
    - cardiovascular: Enfermedades cardiovasculares y cardiológicas
    - neurological: Trastornos neurológicos y neurocientíficos  
    - oncological: Cáncer y oncología
    - hepatorenal: Enfermedades hepáticas y renales
    
    **Retorna:**
    - predicted_class: Categorías predichas separadas por "|" (ej: "cardiovascular|neurological")
    - confidence: Máxima probabilidad entre todas las categorías
    - probabilities: Probabilidades individuales por categoría
    - categories: Lista de categorías que superan el umbral especificado
    
    **Nota:** El modelo puede predecir múltiples categorías simultáneamente si sus probabilidades
    superan el umbral especificado (clasificación multilabel).
    """
    try:
        if not ml_service.is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        prediction = ml_service.predict(request.text, request.threshold)
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
