@echo off
REM 🚀 Script de configuración rápida para TechSphere ML API (Windows)

echo 🚀 Configurando TechSphere ML API...
echo ==================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo    Instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Crear entorno virtual si no existe
if not exist "techsphere-env" (
    echo 📦 Creando entorno virtual...
    python -m venv techsphere-env
    
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b 1
    )
    
    echo ✅ Entorno virtual creado exitosamente
) else (
    echo ✅ Entorno virtual ya existe
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call techsphere-env\Scripts\activate.bat

REM Actualizar pip
echo ⬆️ Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas exitosamente

REM Verificar instalación
echo 🔍 Verificando instalación...
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)" 2>nul
python -c "import torch; print('✅ PyTorch:', torch.__version__)" 2>nul
python -c "import transformers; print('✅ Transformers:', transformers.__version__)" 2>nul

REM Verificar modelo
if exist "scibert_classifier" (
    echo ✅ Modelo SciBERT encontrado
) else (
    echo ❌ Advertencia: Directorio 'scibert_classifier' no encontrado
    echo    Asegúrate de tener el modelo entrenado en este directorio
)

echo.
echo 🎉 ¡Configuración completada exitosamente!
echo.
echo Para usar el proyecto:
echo 1. Activa el entorno virtual: techsphere-env\Scripts\activate
echo 2. Ejecuta la API: python run_api.py
echo 3. Ve a: http://localhost:8000/api/v1/docs
echo.
echo Para desactivar el entorno virtual: deactivate
echo.
pause
