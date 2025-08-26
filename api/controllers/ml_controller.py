"""
Controlador para predicciones del modelo ML
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
import pandas as pd
import io
import time

from ..models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    MetricsResponse, 
    BatchPredictionRequest,
    BatchPredictionResponse
)
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

@router.post(
    "/predict-batch",
    response_model=BatchPredictionResponse,
    summary="Realizar predicción batch desde CSV",
    description="Procesa un archivo CSV con columnas 'title', 'abstract' y 'group' para realizar predicciones multilabel y calcular métricas"
)
async def predict_batch_csv(
    file: UploadFile = File(..., description="Archivo CSV con columnas: title, abstract, group"),
    threshold: Optional[float] = Form(0.5, description="Umbral para clasificación multilabel (0.0-1.0)", ge=0.0, le=1.0)
) -> BatchPredictionResponse:
    """
    Procesa un archivo CSV para realizar predicciones batch y calcular métricas.
    
    **Formato del CSV requerido:**
    - **title**: Título del artículo científico
    - **abstract**: Resumen del artículo científico  
    - **group**: Categorías reales separadas por "|" (ej: "cardiovascular|neurological")
    
    **Proceso:**
    1. Concatena title + abstract para cada fila
    2. Realiza predicción multilabel con el umbral especificado
    3. Calcula métricas comparando group vs group_predicted
    4. Genera archivo CSV con columna adicional "group_predicted"
    
    **Métricas calculadas:**
    - Accuracy, Precision, Recall, F1-score
    - Hamming Loss (específico para multilabel)
    - Exact Match Ratio (coincidencias exactas)
    - Métricas por categoría individual
    
    **Retorna:**
    - Métricas de evaluación completas
    - URL para descargar CSV procesado
    - Tiempo de procesamiento
    """
    start_time = time.time()
    
    try:
        # Validar que el modelo esté cargado
        if not ml_service.is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Modelo no está cargado"
            )
        
        # Validar tipo de archivo
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser un CSV"
            )
        
        # Leer CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validar columnas requeridas
        required_columns = ['title', 'abstract', 'group']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Columnas faltantes en el CSV: {missing_columns}"
            )
        
        # Procesar predicciones batch
        batch_result = ml_service.predict_batch(df, threshold)
        
        processing_time = time.time() - start_time
        
        return BatchPredictionResponse(
            success=True,
            message=f"Procesamiento exitoso de {batch_result['total_processed']} registros",
            total_processed=batch_result['total_processed'],
            metrics=batch_result['metrics'],
            download_url=batch_result['download_url'],
            processing_time=round(processing_time, 2)
        )
        
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo CSV está vacío"
        )
    except pd.errors.ParserError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parseando CSV: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando archivo: {str(e)}"
        )
