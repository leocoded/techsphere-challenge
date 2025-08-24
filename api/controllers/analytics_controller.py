"""
Controlador para análisis y visualizaciones
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..models.schemas import (
    ConfusionMatrixResponse,
    ClassDistributionResponse,
    FeatureImportanceResponse
)
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics & Visualizations"])

@router.get(
    "/confusion-matrix",
    response_model=ConfusionMatrixResponse,
    summary="Matriz de confusión",
    description="Obtiene la matriz de confusión del modelo para visualización"
)
async def get_confusion_matrix() -> ConfusionMatrixResponse:
    """
    Obtiene la matriz de confusión del modelo.
    
    Retorna la matriz y las etiquetas correspondientes para crear visualizaciones.
    """
    try:
        matrix = analytics_service.get_confusion_matrix()
        return matrix
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo matriz de confusión: {str(e)}"
        )

@router.get(
    "/class-distribution",
    response_model=ClassDistributionResponse,
    summary="Distribución de clases",
    description="Obtiene la distribución de clases en el dataset de entrenamiento"
)
async def get_class_distribution() -> ClassDistributionResponse:
    """
    Obtiene la distribución de clases.
    
    Retorna la distribución de clases y el total de muestras para crear gráficos.
    """
    try:
        distribution = analytics_service.get_class_distribution()
        return distribution
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo distribución de clases: {str(e)}"
        )

@router.get(
    "/feature-importance",
    response_model=FeatureImportanceResponse,
    summary="Importancia de características",
    description="Obtiene las características más importantes del modelo"
)
async def get_feature_importance() -> FeatureImportanceResponse:
    """
    Obtiene la importancia de las características.
    
    Retorna las características más importantes identificadas por el modelo.
    """
    try:
        importance = analytics_service.get_feature_importance()
        return importance
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo importancia de características: {str(e)}"
        )

@router.get(
    "/performance-over-time",
    response_model=Dict[str, Any],
    summary="Rendimiento temporal",
    description="Obtiene el rendimiento del modelo a lo largo del tiempo"
)
async def get_performance_over_time() -> Dict[str, Any]:
    """
    Obtiene el rendimiento del modelo a lo largo del tiempo.
    
    Retorna métricas de F1-score y accuracy por fecha para crear gráficos temporales.
    """
    try:
        performance = analytics_service.get_model_performance_over_time()
        return performance
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo rendimiento temporal: {str(e)}"
        )

@router.get(
    "/category-correlations",
    response_model=Dict[str, Any],
    summary="Correlaciones entre categorías",
    description="Obtiene la matriz de correlación entre categorías médicas"
)
async def get_category_correlations() -> Dict[str, Any]:
    """
    Obtiene correlaciones entre categorías médicas.
    
    Retorna una matriz de correlación entre diferentes categorías médicas.
    """
    try:
        correlations = analytics_service.get_category_correlation_matrix()
        return correlations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo correlaciones: {str(e)}"
        )
