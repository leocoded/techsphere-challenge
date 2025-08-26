"""
Ejemplo de cliente para usar TechSphere API con Ngrok
Este script demuestra cómo usar la API cuando está expuesta públicamente
"""
import requests
import json
import sys
import time

def test_ngrok_api(base_url):
    """
    Prueba la API de TechSphere cuando está expuesta con Ngrok
    
    Args:
        base_url (str): URL base de la API (ej: https://abc123.ngrok-free.app)
    """
    
    print(f"🧪 Probando TechSphere API en: {base_url}")
    print("=" * 60)
    
    # 1. Health Check
    print("\n1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/api/v1/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # 2. Información del sistema
    print("\n2. ℹ️  Información del Sistema")
    try:
        response = requests.get(f"{base_url}/api/v1/system/info", timeout=10)
        print(f"   Status: {response.status_code}")
        info = response.json()
        print(f"   App: {info.get('app_name')} v{info.get('version')}")
        print(f"   Modelo: {info.get('model_info', {}).get('model_name', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Métricas del modelo
    print("\n3. 📊 Métricas del Modelo")
    try:
        response = requests.get(f"{base_url}/api/v1/ml/metrics", timeout=10)
        print(f"   Status: {response.status_code}")
        metrics = response.json()
        print(f"   F1-Score: {metrics.get('f1_score', 'N/A')}")
        print(f"   Accuracy: {metrics.get('accuracy', 'N/A')}")
        print(f"   Precision: {metrics.get('precision', 'N/A')}")
        print(f"   Recall: {metrics.get('recall', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Clases disponibles
    print("\n4. 🏷️  Clases Disponibles")
    try:
        response = requests.get(f"{base_url}/api/v1/ml/classes", timeout=10)
        print(f"   Status: {response.status_code}")
        classes = response.json()
        print(f"   Clases: {', '.join(classes.get('classes', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Predicción de ejemplo
    print("\n5. 🤖 Predicción de Ejemplo")
    test_text = """
    Hypothesis: ACE inhibitors improve cardiovascular outcomes in diabetic patients.
    Methods: We conducted a randomized controlled trial with 500 diabetic patients.
    Results: Patients showed significant improvement in cardiac function and reduced mortality.
    """
    
    try:
        payload = {"text": test_text.strip()}
        response = requests.post(
            f"{base_url}/api/v1/ml/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            prediction = response.json()
            print(f"   📝 Texto: '{test_text[:50]}...'")
            print(f"   🎯 Predicción: {prediction.get('predicted_class', 'N/A')}")
            print(f"   📊 Confianza: {prediction.get('confidence', 'N/A'):.3f}")
            print(f"   📈 Probabilidades:")
            for cls, prob in prediction.get('class_probabilities', {}).items():
                print(f"      - {cls}: {prob:.3f}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Analytics
    print("\n6. 📈 Datos de Analytics")
    analytics_endpoints = [
        ("Matriz de Confusión", "/api/v1/analytics/confusion-matrix"),
        ("Distribución de Clases", "/api/v1/analytics/class-distribution"),
        ("Características Importantes", "/api/v1/analytics/feature-importance")
    ]
    
    for name, endpoint in analytics_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"   {name}: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    print(f"      ✅ {len(data['data'])} elementos")
                else:
                    print(f"      ✅ Datos disponibles")
        except Exception as e:
            print(f"   {name}: ❌ Error: {e}")
    
    print(f"\n✅ Prueba completada para: {base_url}")
    print(f"📖 Documentación disponible en: {base_url}/api/v1/docs")
    
    return True

def main():
    """Función principal"""
    print("🌐 Cliente de Prueba para TechSphere API con Ngrok")
    print("=" * 60)
    
    # Obtener URL de la API
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = input("🔗 Introduce la URL de Ngrok (ej: https://abc123.ngrok-free.app): ").rstrip('/')
    
    if not base_url:
        print("❌ URL requerida")
        return
    
    if not base_url.startswith(('http://', 'https://')):
        base_url = f"https://{base_url}"
    
    print(f"🎯 Objetivo: {base_url}")
    print("⏳ Iniciando pruebas...")
    
    # Ejecutar pruebas
    success = test_ngrok_api(base_url)
    
    if success:
        print("\n🎉 ¡Todas las pruebas completadas!")
        print("\n💡 Comandos útiles:")
        print(f"   curl {base_url}/api/v1/health")
        print(f"   curl {base_url}/api/v1/ml/metrics")
        print(f"   open {base_url}/api/v1/docs")
    else:
        print("\n❌ Algunas pruebas fallaron. Verifica:")
        print("   1. Que la API esté corriendo con: python run_api.py --ngrok")
        print("   2. Que la URL de Ngrok sea correcta")
        print("   3. Que no haya problemas de conectividad")

if __name__ == "__main__":
    main()
