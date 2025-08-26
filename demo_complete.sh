#!/bin/bash

# Script de demostración completa de TechSphere API con Ngrok

echo "🚀 Demostración Completa de TechSphere API con Ngrok"
echo "===================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "run_api.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio del proyecto"
    exit 1
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source techsphere-env/bin/activate

# Verificar dependencias
echo "📦 Verificando dependencias..."
python -c "import pyngrok; print('✅ pyngrok instalado')" 2>/dev/null || {
    echo "📥 Instalando pyngrok..."
    pip install pyngrok
}

echo ""
echo "🎯 Opciones de demostración:"
echo "1. 💻 Solo local (http://localhost:8000)"
echo "2. 🌐 Con Ngrok (acceso público)"
echo "3. 🔧 Configurar Ngrok primero"
echo "4. ℹ️  Solo mostrar información"

read -p "Selecciona una opción (1-4): " option

case $option in
    1)
        echo ""
        echo "🚀 Iniciando API localmente..."
        echo "📖 Documentación: http://localhost:8000/api/v1/docs"
        echo "💡 Presiona Ctrl+C para parar"
        python run_api.py
        ;;
    2)
        echo ""
        echo "🌐 Iniciando API con Ngrok..."
        echo "💡 La URL pública se mostrará cuando esté lista"
        echo "💡 Presiona Ctrl+C para parar"
        python run_api.py --ngrok
        ;;
    3)
        echo ""
        echo "🔧 Configurando Ngrok..."
        ./setup_ngrok.sh
        echo ""
        echo "✅ Configuración completada. Ahora puedes ejecutar:"
        echo "   python run_api.py --ngrok"
        ;;
    4)
        echo ""
        echo "📋 Información del Sistema TechSphere API"
        echo "========================================"
        echo ""
        echo "📁 Estructura del proyecto:"
        echo "   ├── api/                 # 🚪 API FastAPI"
        echo "   ├── scibert_classifier/  # 🤖 Modelo entrenado"
        echo "   ├── techsphere-env/      # 🐍 Entorno virtual"
        echo "   ├── run_api.py          # 🚀 Servidor principal"
        echo "   └── ngrok_config.py     # 🌐 Configuración Ngrok"
        echo ""
        echo "🎮 Comandos disponibles:"
        echo "   python run_api.py                    # Solo local"
        echo "   python run_api.py --ngrok            # Con Ngrok"
        echo "   python run_api.py --help             # Ver opciones"
        echo ""
        echo "📊 Endpoints principales:"
        echo "   POST /api/v1/ml/predict             # Clasificar texto"
        echo "   GET  /api/v1/ml/metrics             # Métricas del modelo"
        echo "   GET  /api/v1/analytics/*            # Datos para dashboard"
        echo "   GET  /api/v1/health                 # Health check"
        echo ""
        echo "🧪 Scripts de prueba:"
        echo "   python client_example.py            # Cliente local"
        echo "   python ngrok_client_example.py      # Cliente para Ngrok"
        echo "   python dashboard_example.py         # Generar gráficas"
        echo ""
        echo "📚 Documentación:"
        echo "   📖 USAGE_GUIDE.md      # Guía completa de uso"
        echo "   🌐 NGROK_GUIDE.md      # Guía específica de Ngrok"
        echo "   🔍 README.md           # Información general"
        echo ""
        echo "✨ Funcionalidades implementadas:"
        echo "   ✅ Clasificación de textos científicos médicos"
        echo "   ✅ Métricas de rendimiento del modelo"
        echo "   ✅ Visualizaciones y analytics"
        echo "   ✅ Documentación automática (Swagger/ReDoc)"
        echo "   ✅ Exposición pública con Ngrok"
        echo "   ✅ Clientes de ejemplo"
        echo "   ✅ Dashboard interactivo"
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "👋 ¡Gracias por usar TechSphere API!"
