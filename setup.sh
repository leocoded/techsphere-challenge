#!/bin/bash

# 🚀 Script de configuración rápida para TechSphere ML API

echo "🚀 Configurando TechSphere ML API..."
echo "=================================="

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "   Instala Python 3 desde https://python.org"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "techsphere-env" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv techsphere-env
    
    if [ $? -eq 0 ]; then
        echo "✅ Entorno virtual creado exitosamente"
    else
        echo "❌ Error creando entorno virtual"
        exit 1
    fi
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source techsphere-env/bin/activate

if [ $? -eq 0 ]; then
    echo "✅ Entorno virtual activado"
else
    echo "❌ Error activando entorno virtual"
    exit 1
fi

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas exitosamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)" 2>/dev/null
python -c "import torch; print('✅ PyTorch:', torch.__version__)" 2>/dev/null
python -c "import transformers; print('✅ Transformers:', transformers.__version__)" 2>/dev/null

# Verificar modelo
if [ -d "scibert_classifier" ]; then
    echo "✅ Modelo SciBERT encontrado"
else
    echo "❌ Advertencia: Directorio 'scibert_classifier' no encontrado"
    echo "   Asegúrate de tener el modelo entrenado en este directorio"
fi

echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo ""
echo "Para usar el proyecto:"
echo "1. Activa el entorno virtual: source techsphere-env/bin/activate"
echo "2. Ejecuta la API: python run_api.py"
echo "3. Ve a: http://localhost:8000/api/v1/docs"
echo ""
echo "Para desactivar el entorno virtual: deactivate"
echo ""
