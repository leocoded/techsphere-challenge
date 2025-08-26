"""
Cliente de ejemplo para funcionalidad de procesamiento batch
TechSphere ML API
"""
import requests
import pandas as pd
import json
import time
from pathlib import Path
import sys

# Configuración
API_BASE_URL = "http://localhost:8000/api/v1"
SAMPLE_CSV_FILE = "sample_data.csv"

def create_sample_dataset():
    """Crea un dataset de ejemplo para probar la funcionalidad batch"""
    data = {
        'title': [
            "Mechanisms of myocardial ischemia induced by epinephrine: comparison with exercise-induced ischemia",
            "Brain tumor classification using convolutional neural networks",
            "Hepatocellular carcinoma treatment outcomes with sorafenib therapy",
            "Cardiovascular risk factors in diabetic patients with chronic kidney disease",
            "Neurological complications following cardiac surgery: a systematic review",
            "Liver metastases from colorectal cancer: surgical management and outcomes",
            "Deep learning approaches for Alzheimer's disease detection",
            "Heart failure management with ACE inhibitors",
            "Renal function assessment in chronic kidney disease",
            "Breast cancer screening using AI-powered mammography"
        ],
        'abstract': [
            "The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease. Objective signs of ischemia and factors increasing myocardial oxygen consumption were compared during epinephrine infusion and supine bicycle exercise.",
            "Deep learning approaches have shown promising results in medical image analysis particularly for brain tumor detection and classification. We developed a CNN-based model for automatic brain tumor classification from MRI scans.",
            "This retrospective study analyzed treatment outcomes in patients with advanced hepatocellular carcinoma receiving sorafenib therapy. We evaluated overall survival progression-free survival and adverse events.",
            "This cross-sectional study examined cardiovascular risk factors in diabetic patients with various stages of chronic kidney disease. We assessed the relationship between kidney function and cardiovascular outcomes.",
            "We conducted a systematic review of neurological complications occurring after cardiac surgical procedures including stroke delirium and cognitive dysfunction. The review included studies from the past decade.",
            "This study evaluated surgical outcomes in patients with colorectal liver metastases undergoing hepatic resection. We analyzed factors associated with overall survival and recurrence patterns.",
            "Machine learning algorithms were applied to neuroimaging data for early detection of Alzheimer's disease. We used structural MRI and cognitive assessment scores to build predictive models.",
            "Clinical outcomes of heart failure patients treated with ACE inhibitors were evaluated in this multicenter study. We assessed mortality rates and quality of life measures over 2 years.",
            "We investigated biomarkers for assessing kidney function in patients with chronic kidney disease. Serum creatinine and estimated GFR were compared across different CKD stages.",
            "An artificial intelligence system was developed for automated breast cancer detection in mammographic images. The system achieved high sensitivity and specificity in clinical validation."
        ],
        'group': [
            "cardiovascular",
            "neurological",
            "hepatorenal|oncological",
            "cardiovascular|hepatorenal",
            "cardiovascular|neurological",
            "hepatorenal|oncological",
            "neurological",
            "cardiovascular",
            "hepatorenal",
            "oncological"
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(SAMPLE_CSV_FILE, index=False)
    print(f"✅ Dataset de ejemplo creado: {SAMPLE_CSV_FILE}")
    return df

def check_api_health():
    """Verifica que la API esté funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API funcionando - Status: {data['status']}, Modelo: {'Cargado' if data['model_loaded'] else 'No cargado'}")
            return True
        else:
            print(f"❌ Error en health check: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API. ¿Está corriendo en http://localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def process_batch(csv_file, threshold=0.4):
    """Procesa un archivo CSV usando la funcionalidad batch"""
    print(f"📊 Procesando archivo: {csv_file}")
    print(f"🎯 Umbral configurado: {threshold}")
    
    try:
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            data = {'threshold': threshold}
            
            print("⏳ Enviando archivo para procesamiento...")
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/ml/predict-batch",
                files=files,
                data=data
            )
            
            processing_time = time.time() - start_time
            print(f"⏱️  Tiempo de envío: {processing_time:.2f} segundos")
            
            if response.status_code == 200:
                result = response.json()
                print("\n🎉 ¡Procesamiento exitoso!")
                print(f"📈 Registros procesados: {result['total_processed']}")
                print(f"⏱️  Tiempo total: {result['processing_time']} segundos")
                
                return result
            else:
                print(f"❌ Error en procesamiento: {response.status_code}")
                print(f"Detalle: {response.text}")
                return None
                
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {csv_file}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def display_metrics(metrics):
    """Muestra las métricas de manera legible"""
    if not metrics:
        print("❌ No hay métricas para mostrar")
        return
    
    print("\n📊 MÉTRICAS GENERALES")
    print("=" * 50)
    print(f"🎯 Accuracy:          {metrics['accuracy']:.1%}")
    print(f"🎯 Precision:         {metrics['precision']:.1%}")
    print(f"🎯 Recall:            {metrics['recall']:.1%}")
    print(f"🎯 F1-Score:          {metrics['f1_score']:.1%}")
    print(f"🎯 Hamming Loss:      {metrics['hamming_loss']:.1%}")
    print(f"🎯 Exact Match:       {metrics['exact_match_ratio']:.1%}")
    print(f"📝 Total Muestras:    {metrics['total_samples']}")
    
    print("\n📈 MÉTRICAS POR CATEGORÍA")
    print("=" * 50)
    for category, cat_metrics in metrics['category_metrics'].items():
        print(f"\n🏷️  {category.upper()}")
        print(f"   Precision: {cat_metrics['precision']:.1%}")
        print(f"   Recall:    {cat_metrics['recall']:.1%}")
        print(f"   F1-Score:  {cat_metrics['f1_score']:.1%}")
        print(f"   Support:   {cat_metrics['support']} muestras")

def download_results(download_url, output_filename="batch_results.csv"):
    """Descarga el archivo procesado"""
    try:
        print(f"\n💾 Descargando resultados...")
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}{download_url}")
        
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Resultados guardados en: {output_filename}")
            
            # Mostrar preview del archivo
            try:
                df = pd.read_csv(output_filename)
                print(f"\n📄 PREVIEW DEL ARCHIVO ({len(df)} filas):")
                print("=" * 80)
                print(df[['title', 'group', 'group_predicted', 'confidence']].head())
                
                # Estadísticas rápidas
                print(f"\n📊 ESTADÍSTICAS RÁPIDAS:")
                print(f"   Confianza promedio: {df['confidence'].mean():.3f}")
                print(f"   Confianza máxima:   {df['confidence'].max():.3f}")
                print(f"   Confianza mínima:   {df['confidence'].min():.3f}")
                
                return df
                
            except Exception as e:
                print(f"⚠️  Error mostrando preview: {e}")
                return None
                
        else:
            print(f"❌ Error descargando archivo: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def analyze_results(df):
    """Analiza los resultados del procesamiento"""
    if df is None:
        return
        
    print(f"\n🔍 ANÁLISIS DE RESULTADOS")
    print("=" * 50)
    
    # Coincidencias exactas
    exact_matches = (df['group'] == df['group_predicted']).sum()
    total = len(df)
    print(f"✅ Coincidencias exactas: {exact_matches}/{total} ({exact_matches/total:.1%})")
    
    # Casos con múltiples categorías predichas
    multi_predictions = df['group_predicted'].str.contains('|', na=False).sum()
    print(f"🏷️  Predicciones multilabel: {multi_predictions}/{total} ({multi_predictions/total:.1%})")
    
    # Distribución de confianza
    high_conf = (df['confidence'] >= 0.8).sum()
    med_conf = ((df['confidence'] >= 0.5) & (df['confidence'] < 0.8)).sum()
    low_conf = (df['confidence'] < 0.5).sum()
    
    print(f"\n📊 DISTRIBUCIÓN DE CONFIANZA:")
    print(f"   Alta (≥0.8):   {high_conf} casos ({high_conf/total:.1%})")
    print(f"   Media (0.5-0.8): {med_conf} casos ({med_conf/total:.1%})")
    print(f"   Baja (<0.5):   {low_conf} casos ({low_conf/total:.1%})")

def main():
    """Función principal del cliente de ejemplo"""
    print("🚀 Cliente de Ejemplo - Procesamiento Batch")
    print("TechSphere ML API")
    print("=" * 60)
    
    # Verificar API
    if not check_api_health():
        sys.exit(1)
    
    # Crear dataset de ejemplo si no existe
    if not Path(SAMPLE_CSV_FILE).exists():
        create_sample_dataset()
    
    # Procesar archivo
    result = process_batch(SAMPLE_CSV_FILE, threshold=0.4)
    
    if result and result['success']:
        # Mostrar métricas
        display_metrics(result['metrics'])
        
        # Descargar y analizar resultados
        df = download_results(result['download_url'], "example_batch_results.csv")
        analyze_results(df)
        
        print(f"\n🎉 ¡Proceso completado exitosamente!")
        print(f"📁 Archivo de resultados: example_batch_results.csv")
        
    else:
        print("❌ Error en el procesamiento")

if __name__ == "__main__":
    main()
