"""
Cliente de ejemplo para probar la API de TechSphere
"""
import requests
import json
from typing import Dict, Any

class TechSphereClient:
    """Cliente para interactuar con la API de TechSphere"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar el estado de la API"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_info(self) -> Dict[str, Any]:
        """Obtener información de la API"""
        response = self.session.get(f"{self.base_url}/info")
        response.raise_for_status()
        return response.json()
    
    def predict(self, text: str) -> Dict[str, Any]:
        """Clasificar un texto científico"""
        data = {"text": text}
        response = self.session.post(f"{self.base_url}/ml/predict", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtener métricas del modelo"""
        response = self.session.get(f"{self.base_url}/ml/metrics")
        response.raise_for_status()
        return response.json()
    
    def get_classes(self) -> list:
        """Obtener clases disponibles"""
        response = self.session.get(f"{self.base_url}/ml/classes")
        response.raise_for_status()
        return response.json()
    
    def get_confusion_matrix(self) -> Dict[str, Any]:
        """Obtener matriz de confusión"""
        response = self.session.get(f"{self.base_url}/analytics/confusion-matrix")
        response.raise_for_status()
        return response.json()
    
    def get_class_distribution(self) -> Dict[str, Any]:
        """Obtener distribución de clases"""
        response = self.session.get(f"{self.base_url}/analytics/class-distribution")
        response.raise_for_status()
        return response.json()
    
    def get_feature_importance(self) -> Dict[str, Any]:
        """Obtener importancia de características"""
        response = self.session.get(f"{self.base_url}/analytics/feature-importance")
        response.raise_for_status()
        return response.json()
    
    def get_performance_over_time(self) -> Dict[str, Any]:
        """Obtener rendimiento temporal"""
        response = self.session.get(f"{self.base_url}/analytics/performance-over-time")
        response.raise_for_status()
        return response.json()
    
    def get_category_correlations(self) -> Dict[str, Any]:
        """Obtener correlaciones entre categorías"""
        response = self.session.get(f"{self.base_url}/analytics/category-correlations")
        response.raise_for_status()
        return response.json()

def main():
    """Función principal para probar el cliente"""
    client = TechSphereClient()
    
    print("🔍 TechSphere API Client - Demo")
    print("=" * 50)
    
    try:
        # 1. Health check
        print("\n1. Health Check:")
        health = client.health_check()
        print(f"   Estado: {health['status']}")
        print(f"   Modelo cargado: {health['model_loaded']}")
        
        # 2. Información de la API
        print("\n2. Información de la API:")
        info = client.get_info()
        print(f"   Nombre: {info['app_name']}")
        print(f"   Versión: {info['version']}")
        print(f"   Clases totales: {info['total_classes']}")
        
        # 3. Obtener clases disponibles
        print("\n3. Clases disponibles:")
        classes = client.get_classes()
        for i, cls in enumerate(classes[:5], 1):  # Solo primeras 5
            print(f"   {i}. {cls}")
        if len(classes) > 5:
            print(f"   ... y {len(classes) - 5} más")
        
        # 4. Hacer una predicción
        print("\n4. Predicción de texto:")
        sample_text = """
        Hypothesis: ACE inhibitors improves heart disease outcomes via acute myeloid leukemia pathways. 
        Methods: randomized controlled trial with 264 diabetic patients, measuring interstitial nephritis and kidney. 
        Results: better quality of life measures. 
        Conclusion: cost-effectiveness implications.
        """
        
        prediction = client.predict(sample_text.strip())
        print(f"   Texto: {sample_text.strip()[:100]}...")
        print(f"   Predicción: {prediction['predicted_class']}")
        print(f"   Confianza: {prediction['confidence']:.3f}")
        print(f"   Categorías: {', '.join(prediction['categories'])}")
        
        # 5. Métricas del modelo
        print("\n5. Métricas del modelo:")
        metrics = client.get_metrics()
        print(f"   F1-Score: {metrics['f1_score']:.3f}")
        print(f"   Accuracy: {metrics['accuracy']:.3f}")
        print(f"   Precision: {metrics['precision']:.3f}")
        print(f"   Recall: {metrics['recall']:.3f}")
        
        # 6. Distribución de clases
        print("\n6. Distribución de clases (top 5):")
        distribution = client.get_class_distribution()
        sorted_dist = sorted(distribution['distribution'].items(), 
                           key=lambda x: x[1], reverse=True)
        for class_name, count in sorted_dist[:5]:
            print(f"   {class_name}: {count} muestras")
        print(f"   Total de muestras: {distribution['total_samples']}")
        
        # 7. Importancia de características
        print("\n7. Características más importantes (top 5):")
        importance = client.get_feature_importance()
        for feature in importance['features'][:5]:
            print(f"   {feature['rank']}. {feature['feature']}: {feature['importance']:.3f}")
        
        print(f"\n✅ Demo completada exitosamente!")
        print(f"📖 Para más detalles, visita: http://localhost:8000/api/v1/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API.")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
