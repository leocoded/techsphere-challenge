"""
Servicio para análisis y visualizaciones
"""
import json
import numpy as np
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime

from ..core.utils import MLUtils
from ..models.schemas import (
    ConfusionMatrixResponse, 
    ClassDistributionResponse, 
    FeatureImportanceResponse
)

class AnalyticsService:
    """Servicio para análisis de datos y métricas"""
    
    def __init__(self):
        self.sample_data = self._generate_sample_data()
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Genera datos de muestra para visualizaciones"""
        categories = ["cardiovascular", "neurological", "oncological", "hepatorenal"]
        
        # Distribución de clases simulada
        distribution = {
            "cardiovascular": 180,
            "neurological": 145,
            "oncological": 120,
            "hepatorenal": 95,
            "cardiovascular|neurological": 75,
            "cardiovascular|oncological": 55,
            "neurological|oncological": 40,
            "hepatorenal|oncological": 35,
            "cardiovascular|hepatorenal": 30,
            "neurological|hepatorenal": 25
        }
        
        return {
            "distribution": distribution,
            "categories": categories,
            "total_samples": sum(distribution.values())
        }
    
    def get_confusion_matrix(self) -> ConfusionMatrixResponse:
        """Genera una matriz de confusión simulada"""
        categories = self.sample_data["categories"]
        n_classes = len(categories)
        
        # Generar matriz de confusión simulada
        matrix = []
        for i in range(n_classes):
            row = []
            for j in range(n_classes):
                if i == j:  # Diagonal principal (predicciones correctas)
                    value = random.randint(80, 120)
                elif abs(i - j) == 1:  # Clases adyacentes (confusiones comunes)
                    value = random.randint(5, 15)
                else:  # Otras confusiones
                    value = random.randint(0, 5)
                row.append(value)
            matrix.append(row)
        
        return ConfusionMatrixResponse(
            matrix=matrix,
            labels=categories
        )
    
    def get_class_distribution(self) -> ClassDistributionResponse:
        """Obtiene la distribución de clases"""
        return ClassDistributionResponse(
            distribution=self.sample_data["distribution"],
            total_samples=self.sample_data["total_samples"]
        )
    
    def get_feature_importance(self) -> FeatureImportanceResponse:
        """Obtiene características más importantes (simulado)"""
        
        # Características médicas importantes simuladas
        medical_terms = [
            "randomized controlled trial",
            "systematic review",
            "meta-analysis",
            "clinical efficacy",
            "adverse effects",
            "therapeutic intervention",
            "diagnostic accuracy",
            "prognostic factors",
            "treatment outcomes",
            "biomarkers",
            "pharmacokinetics",
            "dose-response",
            "placebo-controlled",
            "double-blind",
            "statistical significance",
            "confidence interval",
            "hazard ratio",
            "relative risk",
            "sensitivity",
            "specificity"
        ]
        
        features = []
        for i, term in enumerate(medical_terms[:15]):  # Top 15 características
            importance = round(random.uniform(0.1, 0.9), 3)
            features.append({
                "feature": term,
                "importance": importance,
                "rank": i + 1,
                "category": "medical_terminology" if i < 10 else "statistical_methods"
            })
        
        # Ordenar por importancia
        features.sort(key=lambda x: x["importance"], reverse=True)
        
        # Actualizar ranks después del ordenamiento
        for i, feature in enumerate(features):
            feature["rank"] = i + 1
        
        return FeatureImportanceResponse(
            features=features,
            method="SHAP_values_simulation"
        )
    
    def get_model_performance_over_time(self) -> Dict[str, Any]:
        """Genera datos de rendimiento del modelo a lo largo del tiempo (simulado)"""
        dates = []
        f1_scores = []
        accuracies = []
        
        # Generar 30 puntos de datos para el último mes
        base_date = datetime.now()
        for i in range(30):
            date = base_date.replace(day=1).replace(day=i+1)
            dates.append(date.strftime("%Y-%m-%d"))
            
            # Simular fluctuaciones realistas en métricas
            f1_base = 0.89
            acc_base = 0.92
            
            f1_noise = random.uniform(-0.03, 0.03)
            acc_noise = random.uniform(-0.02, 0.02)
            
            f1_scores.append(round(f1_base + f1_noise, 3))
            accuracies.append(round(acc_base + acc_noise, 3))
        
        return {
            "dates": dates,
            "f1_scores": f1_scores,
            "accuracies": accuracies,
            "average_f1": round(np.mean(f1_scores), 3),
            "average_accuracy": round(np.mean(accuracies), 3)
        }
    
    def get_category_correlation_matrix(self) -> Dict[str, Any]:
        """Genera matriz de correlación entre categorías médicas"""
        categories = self.sample_data["categories"]
        n_categories = len(categories)
        
        # Generar matriz de correlación simulada
        correlation_matrix = []
        for i in range(n_categories):
            row = []
            for j in range(n_categories):
                if i == j:
                    correlation = 1.0
                elif (categories[i] == "cardiovascular" and categories[j] == "neurological") or \
                     (categories[i] == "neurological" and categories[j] == "cardiovascular"):
                    correlation = 0.45  # Alta correlación conocida
                elif (categories[i] == "oncological" and categories[j] == "hepatorenal") or \
                     (categories[i] == "hepatorenal" and categories[j] == "oncological"):
                    correlation = 0.35
                else:
                    correlation = round(random.uniform(0.1, 0.3), 2)
                row.append(correlation)
            correlation_matrix.append(row)
        
        return {
            "matrix": correlation_matrix,
            "labels": categories,
            "method": "pearson_correlation"
        }

# Instancia global del servicio
analytics_service = AnalyticsService()
