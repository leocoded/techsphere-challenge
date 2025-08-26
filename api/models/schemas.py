"""
Modelos de datos para las solicitudes y respuestas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class PredictionRequest(BaseModel):
    """Modelo para solicitudes de predicción"""
    text: str = Field(
        ..., 
        description="Texto científico completo formado por la concatenación del título (title) y resumen (abstract) del artículo científico. Formato: '{title} {abstract}'", 
        min_length=10, 
        max_length=5000
    )
    threshold: Optional[float] = Field(
        default=0.5, 
        description="Umbral de confianza para clasificación multilabel (0.0-1.0). Categorías con probabilidad >= threshold serán incluidas en la predicción", 
        ge=0.0, 
        le=1.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Mechanisms of myocardial ischemia induced by epinephrine: comparison with exercise-induced ischemia The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease. Objective signs of ischemia and factors increasing myocardial oxygen consumption were compared during epinephrine infusion and supine bicycle exercise.",
                "threshold": 0.5
            }
        }

class PredictionResponse(BaseModel):
    """Modelo para respuestas de predicción"""
    predicted_class: str = Field(..., description="Clase predicha")
    confidence: float = Field(..., description="Confianza de la predicción", ge=0.0, le=1.0)
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    categories: List[str] = Field(..., description="Categorías individuales identificadas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_class": "cardiovascular|neurological",
                "confidence": 0.87,
                "probabilities": {
                    "cardiovascular": 0.45,
                    "neurological": 0.42,
                    "oncological": 0.13
                },
                "categories": ["cardiovascular", "neurological"]
            }
        }

class MetricsResponse(BaseModel):
    """Modelo para métricas del modelo"""
    f1_score: float = Field(..., description="F1-score del modelo")
    accuracy: float = Field(..., description="Accuracy del modelo")
    precision: float = Field(..., description="Precision del modelo")
    recall: float = Field(..., description="Recall del modelo")
    total_classes: int = Field(..., description="Número total de clases")
    
class ConfusionMatrixResponse(BaseModel):
    """Modelo para matriz de confusión"""
    matrix: List[List[int]] = Field(..., description="Matriz de confusión")
    labels: List[str] = Field(..., description="Etiquetas de las clases")
    
class ConfusionMatrixMetricsResponse(BaseModel):
    """Modelo para métricas de matriz de confusión por categoría"""
    category_metrics: Dict[str, Dict[str, int]] = Field(..., description="Métricas TN, FP, FN, TP por categoría")
    categories: List[str] = Field(..., description="Lista de categorías")
    
class ClassDistributionResponse(BaseModel):
    """Modelo para distribución de clases"""
    distribution: Dict[str, int] = Field(..., description="Distribución de clases")
    total_samples: int = Field(..., description="Total de muestras")

class FeatureImportanceResponse(BaseModel):
    """Modelo para importancia de características"""
    features: List[Dict[str, Any]] = Field(..., description="Características más importantes")
    method: str = Field(..., description="Método usado para calcular importancia")
    
class HealthResponse(BaseModel):
    """Modelo para respuesta de health check"""
    status: str = Field(..., description="Estado del servicio")
    model_loaded: bool = Field(..., description="Si el modelo está cargado")
    timestamp: str = Field(..., description="Timestamp del check")
    version: str = Field(..., description="Versión de la API")
