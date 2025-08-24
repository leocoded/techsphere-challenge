"""
Dashboard simple usando la API de TechSphere para crear visualizaciones
"""
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, Any

class TechSphereDashboard:
    """Dashboard para visualizar datos de la API TechSphere"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Configurar estilo de las gráficas
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def _get_data(self, endpoint: str) -> Dict[str, Any]:
        """Obtener datos de un endpoint"""
        response = self.session.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()
    
    def create_metrics_dashboard(self) -> None:
        """Crear dashboard principal con métricas"""
        # Obtener datos
        metrics = self._get_data("/ml/metrics")
        
        # Crear figura con subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('TechSphere ML Model - Métricas Principales', fontsize=16, fontweight='bold')
        
        # 1. Métricas generales (gráfico de barras)
        metric_names = ['F1-Score', 'Accuracy', 'Precision', 'Recall']
        metric_values = [
            metrics['f1_score'], 
            metrics['accuracy'], 
            metrics['precision'], 
            metrics['recall']
        ]
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        bars = ax1.bar(metric_names, metric_values, color=colors, alpha=0.8)
        ax1.set_title('Métricas de Rendimiento del Modelo', fontweight='bold')
        ax1.set_ylabel('Puntuación')
        ax1.set_ylim(0, 1)
        
        # Agregar valores en las barras
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Distribución de clases
        distribution = self._get_data("/analytics/class-distribution")
        
        # Top 8 clases para evitar saturación
        sorted_dist = sorted(distribution['distribution'].items(), 
                           key=lambda x: x[1], reverse=True)[:8]
        
        classes = [item[0] for item in sorted_dist]
        counts = [item[1] for item in sorted_dist]
        
        # Crear gráfico de pie
        ax2.pie(counts, labels=[cls[:15] + '...' if len(cls) > 15 else cls for cls in classes], 
               autopct='%1.1f%%', startangle=90)
        ax2.set_title('Distribución de Clases (Top 8)', fontweight='bold')
        
        # 3. Importancia de características
        importance = self._get_data("/analytics/feature-importance")
        top_features = importance['features'][:10]  # Top 10
        
        feature_names = [f['feature'][:20] + '...' if len(f['feature']) > 20 else f['feature'] 
                        for f in top_features]
        importance_scores = [f['importance'] for f in top_features]
        
        y_pos = np.arange(len(feature_names))
        bars = ax3.barh(y_pos, importance_scores, color='lightblue', alpha=0.8)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(feature_names)
        ax3.set_xlabel('Importancia')
        ax3.set_title('Top 10 Características Más Importantes', fontweight='bold')
        
        # Agregar valores en las barras
        for i, (bar, score) in enumerate(zip(bars, importance_scores)):
            width = bar.get_width()
            ax3.text(width + 0.01, bar.get_y() + bar.get_height()/2.,
                    f'{score:.3f}', ha='left', va='center', fontsize=8)
        
        # 4. Rendimiento temporal
        performance = self._get_data("/analytics/performance-over-time")
        
        dates = performance['dates'][-10:]  # Últimos 10 días
        f1_scores = performance['f1_scores'][-10:]
        accuracies = performance['accuracies'][-10:]
        
        x = range(len(dates))
        ax4.plot(x, f1_scores, marker='o', label='F1-Score', linewidth=2)
        ax4.plot(x, accuracies, marker='s', label='Accuracy', linewidth=2)
        ax4.set_xlabel('Últimos 10 días')
        ax4.set_ylabel('Puntuación')
        ax4.set_title('Tendencia de Rendimiento', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0.8, 1.0)
        
        plt.tight_layout()
        plt.savefig('techsphere_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_confusion_matrix_plot(self) -> None:
        """Crear visualización de matriz de confusión"""
        confusion_data = self._get_data("/analytics/confusion-matrix")
        
        matrix = np.array(confusion_data['matrix'])
        labels = [label[:10] + '...' if len(label) > 10 else label 
                 for label in confusion_data['labels']]
        
        plt.figure(figsize=(12, 10))
        
        # Crear heatmap
        sns.heatmap(matrix, 
                   annot=True, 
                   fmt='d', 
                   cmap='Blues', 
                   xticklabels=labels, 
                   yticklabels=labels,
                   cbar_kws={'label': 'Número de Predicciones'})
        
        plt.title('Matriz de Confusión del Modelo SciBERT', fontsize=16, fontweight='bold')
        plt.xlabel('Predicción', fontweight='bold')
        plt.ylabel('Verdadero', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_correlation_matrix(self) -> None:
        """Crear matriz de correlación entre categorías"""
        correlation_data = self._get_data("/analytics/category-correlations")
        
        matrix = np.array(correlation_data['matrix'])
        labels = correlation_data['labels']
        
        plt.figure(figsize=(10, 8))
        
        # Crear heatmap de correlación
        sns.heatmap(matrix, 
                   annot=True, 
                   fmt='.2f', 
                   cmap='RdBu_r', 
                   center=0,
                   xticklabels=labels, 
                   yticklabels=labels,
                   cbar_kws={'label': 'Correlación'})
        
        plt.title('Matriz de Correlación entre Categorías Médicas', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Categorías', fontweight='bold')
        plt.ylabel('Categorías', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def predict_and_visualize(self, text: str) -> None:
        """Hacer una predicción y visualizar resultados"""
        # Hacer predicción
        prediction_data = {"text": text}
        response = self.session.post(f"{self.base_url}/ml/predict", json=prediction_data)
        response.raise_for_status()
        prediction = response.json()
        
        # Crear visualización
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. Probabilidades por categoría
        categories = list(prediction['probabilities'].keys())
        probabilities = list(prediction['probabilities'].values())
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        bars = ax1.bar(categories, probabilities, color=colors, alpha=0.8)
        ax1.set_title('Probabilidades por Categoría', fontweight='bold')
        ax1.set_xlabel('Categorías Médicas')
        ax1.set_ylabel('Probabilidad')
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for bar, prob in zip(bars, probabilities):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.3f}', ha='center', va='bottom', fontsize=10)
        
        # 2. Información de la predicción
        ax2.axis('off')
        info_text = f"""
        PREDICCIÓN RESULTANTE:
        
        📝 Texto analizado:
        {text[:100]}{'...' if len(text) > 100 else ''}
        
        🎯 Clase predicha:
        {prediction['predicted_class']}
        
        🔍 Confianza:
        {prediction['confidence']:.3f} ({prediction['confidence']*100:.1f}%)
        
        🏷️ Categorías identificadas:
        {', '.join(prediction['categories'])}
        
        📊 Top 3 probabilidades:
        """
        
        # Agregar top 3 probabilidades
        sorted_probs = sorted(prediction['probabilities'].items(), 
                             key=lambda x: x[1], reverse=True)[:3]
        
        for i, (cat, prob) in enumerate(sorted_probs, 1):
            info_text += f"\n    {i}. {cat}: {prob:.3f}"
        
        ax2.text(0.1, 0.9, info_text, transform=ax2.transAxes, 
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('prediction_result.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return prediction

def main():
    """Función principal para crear el dashboard"""
    print("🎨 Creando TechSphere Dashboard...")
    
    try:
        dashboard = TechSphereDashboard()
        
        print("\n1. Creando dashboard de métricas principales...")
        dashboard.create_metrics_dashboard()
        
        print("\n2. Creando matriz de confusión...")
        dashboard.create_confusion_matrix_plot()
        
        print("\n3. Creando matriz de correlación...")
        dashboard.create_correlation_matrix()
        
        print("\n4. Probando predicción con visualización...")
        sample_text = """
        Background: Cardiovascular disease remains a leading cause of mortality worldwide. 
        Objective: To evaluate the efficacy of ACE inhibitors in reducing cardiovascular events 
        in patients with diabetes. Methods: Double-blind randomized controlled trial with 1,200 
        diabetic patients followed for 5 years. Results: ACE inhibitor group showed 23% reduction 
        in major cardiovascular events (p<0.001). Conclusion: ACE inhibitors significantly 
        improve cardiovascular outcomes in diabetic patients.
        """
        
        prediction = dashboard.predict_and_visualize(sample_text.strip())
        
        print(f"\n✅ Dashboard creado exitosamente!")
        print(f"📊 Archivos generados:")
        print(f"   - techsphere_dashboard.png (Dashboard principal)")
        print(f"   - confusion_matrix.png (Matriz de confusión)")
        print(f"   - correlation_matrix.png (Correlaciones)")
        print(f"   - prediction_result.png (Resultado de predicción)")
        
        print(f"\n🔮 Predicción del texto de ejemplo:")
        print(f"   Clase: {prediction['predicted_class']}")
        print(f"   Confianza: {prediction['confidence']:.3f}")
        print(f"   Categorías: {', '.join(prediction['categories'])}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API.")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
