"""
Servicio para el modelo de Machine Learning
"""
import torch
import json
import numpy as np
import logging
from typing import Dict, List, Tuple, Any
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

from ..core.config import config
from ..core.utils import MLUtils, MetricsCalculator
from ..models.schemas import PredictionResponse, MetricsResponse

logger = logging.getLogger(__name__)

class MLModelService:
    """Servicio para el modelo de Machine Learning"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.labels = None
        self.device = None
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo y tokenizer"""
        try:
            model_path = config.get_model_path()
            
            # Cargar tokenizer y modelo
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            
            # Configurar device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            # Cargar etiquetas (incluyendo None/NaN para mantener índices correctos)
            with open(Path(model_path) / "label_encoder.json", "r") as f:
                all_labels = json.load(f)
            self.labels = np.array(all_labels)  # Mantener todas las etiquetas con índices originales
            
            logger.info(f"Modelo cargado exitosamente en {self.device}")
            logger.info(f"Clases disponibles: {len(self.labels)}")
            
        except Exception as e:
            logger.error(f"Error cargando modelo: {str(e)}")
            raise
    
    def predict(self, text: str) -> PredictionResponse:
        """Realiza predicción sobre un texto"""
        try:
            # Tokenizar texto
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=config.MAX_TEXT_LENGTH
            ).to(self.device)
            
            # Realizar predicción
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits, dim=1)
                
            # Obtener predicción
            predicted_idx = torch.argmax(logits, dim=1).item()
            confidence = probabilities[0][predicted_idx].item()
            
            # Manejar caso de predicción NaN/None
            predicted_class = self.labels[predicted_idx]
            if predicted_class is None or (isinstance(predicted_class, str) and predicted_class in ['NaN', 'nan']):
                predicted_class = "unknown"
                categories = ["unknown"]
            else:
                categories = MLUtils.parse_multilabel(predicted_class)
            
            # Calcular probabilidades por clase
            probs_dict = {}
            unique_categories = MLUtils.get_unique_categories(
                [label for label in self.labels.tolist() if label is not None and str(label) != 'nan']
            )
            
            for category in unique_categories:
                category_prob = 0.0
                for i, label in enumerate(self.labels):
                    if label is not None and str(label) != 'nan' and category in MLUtils.parse_multilabel(label):
                        category_prob += probabilities[0][i].item()
                probs_dict[category] = round(category_prob, 4)
            
            return PredictionResponse(
                predicted_class=predicted_class,
                confidence=round(confidence, 4),
                probabilities=probs_dict,
                categories=categories
            )
            
        except Exception as e:
            logger.error(f"Error en predicción: {str(e)}")
            raise
    
    def get_model_metrics(self) -> MetricsResponse:
        """Obtiene métricas del modelo"""
        # Para demo, usamos métricas simuladas
        return MetricsResponse(
            f1_score=0.89,
            accuracy=0.92,
            precision=0.91,
            recall=0.87,
            total_classes=len(self.labels)
        )
    
    def get_class_distribution(self) -> Dict[str, int]:
        """Obtiene distribución simulada de clases para demo"""
        unique_categories = MLUtils.get_unique_categories(self.labels.tolist())
        
        # Distribución simulada
        distribution = {}
        base_counts = [150, 120, 95, 80, 65, 45, 30, 25, 20, 15]
        
        for i, category in enumerate(unique_categories):
            if i < len(base_counts):
                distribution[category] = base_counts[i]
            else:
                distribution[category] = 10
                
        return distribution
    
    def is_model_loaded(self) -> bool:
        """Verifica si el modelo está cargado"""
        return self.model is not None and self.tokenizer is not None
    
    def get_available_classes(self) -> List[str]:
        """Obtiene las clases disponibles"""
        if self.labels is None:
            return []
        return [label for label in self.labels.tolist() if label is not None and str(label) != 'nan']

# Instancia global del servicio
ml_service = MLModelService()
