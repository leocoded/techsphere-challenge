"""
Utilidades comunes para la aplicación
"""
import json
import numpy as np
from typing import List, Dict, Any
from pathlib import Path

class MLUtils:
    """Utilidades para el modelo de ML"""
    
    @staticmethod
    def load_labels(model_path: str) -> np.ndarray:
        """Carga las etiquetas del modelo"""
        with open(Path(model_path) / "label_encoder.json", "r") as f:
            labels = json.load(f)
        return np.array([label for label in labels if label is not None])
    
    @staticmethod
    def clean_labels(labels: List[str]) -> List[str]:
        """Limpia las etiquetas eliminando valores nulos"""
        return [label for label in labels if label is not None and label != 'NaN']
    
    @staticmethod
    def parse_multilabel(label: str) -> List[str]:
        """Parsea etiquetas multilabel separadas por |"""
        if not label or label == 'NaN':
            return []
        return label.split('|')
    
    @staticmethod
    def get_unique_categories(labels: List[str]) -> List[str]:
        """Obtiene categorías únicas de etiquetas multilabel"""
        categories = set()
        for label in labels:
            if label and label != 'NaN':
                categories.update(label.split('|'))
        return sorted(list(categories))

class MetricsCalculator:
    """Calculadora de métricas"""
    
    @staticmethod
    def calculate_f1_score(y_true: List[int], y_pred: List[int]) -> float:
        """Calcula F1-score simulado para demo"""
        # Para propósitos de demo, retornamos un valor simulado
        return 0.89
    
    @staticmethod
    def calculate_accuracy(y_true: List[int], y_pred: List[int]) -> float:
        """Calcula accuracy simulado para demo"""
        # Para propósitos de demo, retornamos un valor simulado
        return 0.92
    
    @staticmethod
    def calculate_precision(y_true: List[int], y_pred: List[int]) -> float:
        """Calcula precision simulado para demo"""
        return 0.91
    
    @staticmethod
    def calculate_recall(y_true: List[int], y_pred: List[int]) -> float:
        """Calcula recall simulado para demo"""
        return 0.87
