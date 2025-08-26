# TechSphere ML API

API para análisis de textos científicos utilizando SciBERT con arquitectura por capas y **soporte para exposición pública con Ngrok**.

## 🚀 Características

- **Clasificación de textos científicos** con modelo SciBERT entrenado
- **🆕 Procesamiento batch de archivos CSV** con métricas de evaluación
- **🆕 Descarga de resultados procesados** con predicciones multilabel
- **Dashboard interactivo** con métricas principales (F1-score, Accuracy)
- **Matriz de confusión visual** para análisis de rendimiento
- **Gráficos de distribución** de clases médicas
- **Demo funcional** para probar clasificaciones en tiempo real
- **Visualización de características** más importantes del modelo
- **🌐 Exposición pública con Ngrok** para acceso desde internet
- **📊 Panel de monitoreo** de túneles Ngrok en tiempo real
- **📈 Métricas multilabel avanzadas** (Hamming Loss, Exact Match Ratio)
- **⚡ Clasificación con umbral configurable** para ajustar sensibilidad

## 🏗️ Arquitectura

La API sigue una arquitectura por capas bien definida:

```
api/
├── controllers/     # Manejo de solicitudes HTTP
├── services/       # Lógica de negocio
├── models/         # Estructuras de datos y validación
└── core/          # Configuración y utilidades
```

### Capas:

- **Controllers**: Manejan solicitudes y respuestas HTTP
- **Services**: Implementan lógica de negocio y coordinan operaciones
- **Models**: Definen estructuras de datos y reglas de validación con Pydantic
- **Core**: Proporcionan utilidades y configuración fundamentales

## 📦 Instalación

### Opción 1: Con Virtual Environment (Recomendado) 🐍

1. **Clonar el repositorio** (o usar el directorio actual)

2. **Crear y activar entorno virtual**:

   ```bash
   # Crear entorno virtual
   python -m venv techsphere-env

   # Activar entorno virtual
   # En macOS/Linux:
   source techsphere-env/bin/activate

   # En Windows:
   techsphere-env\Scripts\activate

   # Verificar que está activado (debería aparecer (techsphere-env) en el prompt)
   ```

3. **Actualizar pip e instalar dependencias**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verificar que el modelo está disponible**:
   ```bash
   ls scibert_classifier/
   ```
   Debe contener: `config.json`, `model.safetensors`, `tokenizer.json`, etc.

### 📥 Descarga del Modelo

Si el modelo no está disponible en el directorio `scibert_classifier/`, puedes descargarlo desde las siguientes ubicaciones:

- **Google Drive**: [Descargar modelo completo](https://drive.google.com/file/d/161MIKh6qFXaviPqEy5r6KW1xvzpX4pNf/view?usp=drive_link)
- **Hugging Face**: [Ver en Hugging Face Hub](https://huggingface.co/mateobravor/tech-sphere-challenge/tree/main)

**Instrucciones de descarga**:

1. **Desde Google Drive**: Descarga el archivo comprimido y extrae el contenido en el directorio `scibert_classifier/`
2. **Desde Hugging Face**: Clona el repositorio o descarga los archivos individuales:

   ```bash
   # Opción 1: Clonar con git-lfs
   git lfs clone https://huggingface.co/mateobravor/tech-sphere-challenge

   # Opción 2: Usar huggingface-hub
   pip install huggingface-hub
   huggingface-cli download mateobravor/tech-sphere-challenge --local-dir ./scibert_classifier
   ```

### Opción 2: Con Conda (Alternativa recomendada) 🐍

```bash
# Crear entorno conda
conda create -n techsphere python=3.10

# Activar entorno
conda activate techsphere

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 3: Instalación Global (No recomendado) ⚠️

Si prefieres instalar globalmente:

```bash
pip install -r requirements.txt
```

**Nota**: La instalación global puede causar conflictos con otros proyectos Python.

### ✅ Verificar Instalación

```bash
# Verificar que FastAPI se instaló correctamente
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"

# Verificar que PyTorch se instaló correctamente
python -c "import torch; print('PyTorch version:', torch.__version__)"

# Verificar que transformers se instaló correctamente
python -c "import transformers; print('Transformers version:', transformers.__version__)"
```

## 🚀 Uso

### Activar Entorno Virtual

**¡IMPORTANTE!** Siempre activa el entorno virtual antes de ejecutar el proyecto:

```bash
# Si usaste venv:
source techsphere-env/bin/activate

# Si usaste conda:
conda activate techsphere

# Verificar que está activado (debe aparecer el nombre del entorno en el prompt)
```

### Ejecutar la API

#### 💻 Ejecución Local

```bash
# Opción 1: Usando el script
python run_api.py

# Opción 2: Usando uvicorn directamente
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://localhost:8000`

#### 🌐 Ejecución Pública con Ngrok

Para hacer tu API accesible desde internet:

```bash
# Configuración rápida (solo la primera vez)
./setup_ngrok.sh

# Ejecutar con Ngrok
python run_api.py --ngrok

# Con token específico
python run_api.py --ngrok --ngrok-token TU_TOKEN

# Puerto personalizado
python run_api.py --ngrok --port 8080
```

**Cuando uses Ngrok obtendrás:**

- 🌐 **URL pública**: `https://abc123.ngrok-free.app`
- 📖 **Documentación**: `https://abc123.ngrok-free.app/api/v1/docs`
- 🔧 **Panel de control**: `http://localhost:4040`

**Comandos útiles:**

```bash
# Ver opciones disponibles
python run_api.py --help

# Demostración completa interactiva
./demo_complete.sh

# Probar API pública
python ngrok_client_example.py https://tu-url-ngrok.app
```

### Documentación interactiva

- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

### Desactivar Entorno Virtual

Cuando termines de trabajar:

```bash
# Para venv y conda:
deactivate
```

## 📋 Endpoints principales

### 🤖 Machine Learning

- `POST /api/v1/ml/predict` - Clasificar texto científico individual
- `POST /api/v1/ml/predict-batch` - **NUEVO**: Clasificar lote de textos desde CSV
- `GET /api/v1/ml/download/{filename}` - **NUEVO**: Descargar archivo procesado
- `GET /api/v1/ml/metrics` - Obtener métricas del modelo
- `GET /api/v1/ml/classes` - Listar clases disponibles

### 📊 Analytics & Visualizaciones

- `GET /api/v1/analytics/confusion-matrix` - Matriz de confusión
- `GET /api/v1/analytics/class-distribution` - Distribución de clases
- `GET /api/v1/analytics/feature-importance` - Características importantes
- `GET /api/v1/analytics/performance-over-time` - Rendimiento temporal
- `GET /api/v1/analytics/category-correlations` - Correlaciones entre categorías

### 🔧 System

- `GET /api/v1/health` - Health check
- `GET /api/v1/info` - Información de la API

## 🧪 Ejemplo de uso

### Clasificar texto científico individual

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Mechanisms of myocardial ischemia induced by epinephrine: comparison with exercise-induced ischemia The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease. Objective signs of ischemia and factors increasing myocardial oxygen consumption were compared during epinephrine infusion and supine bicycle exercise.",
       "threshold": 0.5
     }'
```

### 🆕 **Clasificar lote de textos desde CSV**

**Paso 1: Preparar archivo CSV**

Crear un archivo `data.csv` con las siguientes columnas requeridas:

- `title`: Título del artículo científico
- `abstract`: Resumen del artículo científico
- `group`: Categorías reales (separadas por "|" para multilabel, ej: "cardiovascular|neurological")

```csv
title,abstract,group
"Mechanisms of myocardial ischemia","The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease...","cardiovascular"
"Brain tumor classification","Deep learning approaches have shown promising results in medical image analysis particularly for brain tumor detection...","neurological"
"Hepatocellular carcinoma treatment","This retrospective study analyzed treatment outcomes in patients with advanced hepatocellular carcinoma...","hepatorenal|oncological"
```

**Paso 2: Enviar archivo CSV para procesamiento**

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict-batch" \
     -H "accept: application/json" \
     -F "file=@data.csv" \
     -F "threshold=0.4"
```

**Paso 3: Descargar archivo procesado**

```bash
# Usar la URL proporcionada en la respuesta
curl -X GET "http://localhost:8000/api/v1/ml/download/predictions_YYYYMMDD_HHMMSS.csv" \
     --output predictions_results.csv
```

**Resultado**: El archivo descargado incluirá las columnas originales más:

- `group_predicted`: Categorías predichas por el modelo
- `confidence`: Nivel de confianza de la predicción
- `combined_text`: Texto combinado usado para la predicción (title + abstract)

### Obtener métricas del modelo

```bash
curl "http://localhost:8000/api/v1/ml/metrics"
```

### Obtener matriz de confusión

```bash
curl "http://localhost:8000/api/v1/analytics/confusion-matrix"
```

## 🎯 Categorías de clasificación

El modelo clasifica textos en las siguientes categorías médicas:

- **cardiovascular**: Estudios del sistema cardiovascular
- **neurological**: Investigaciones del sistema nervioso
- **oncological**: Estudios relacionados con cáncer
- **hepatorenal**: Investigaciones de hígado y riñones

También identifica **combinaciones** de categorías (clasificación multilabel).

## 🔍 Estructura de respuestas

### Predicción individual

```json
{
  "predicted_class": "cardiovascular|neurological",
  "confidence": 0.87,
  "probabilities": {
    "cardiovascular": 0.45,
    "neurological": 0.42,
    "oncological": 0.13,
    "hepatorenal": 0.05
  },
  "categories": ["cardiovascular", "neurological"]
}
```

### 🆕 **Predicción batch**

```json
{
  "success": true,
  "message": "Procesamiento exitoso de 6 registros",
  "total_processed": 6,
  "metrics": {
    "accuracy": 0.9167,
    "precision": 0.9167,
    "recall": 0.9167,
    "f1_score": 0.9,
    "hamming_loss": 0.0833,
    "exact_match_ratio": 0.6667,
    "total_samples": 6,
    "category_metrics": {
      "cardiovascular": {
        "precision": 1.0,
        "recall": 0.6667,
        "f1_score": 0.8,
        "support": 3
      },
      "neurological": {
        "precision": 1.0,
        "recall": 1.0,
        "f1_score": 1.0,
        "support": 2
      },
      "hepatorenal": {
        "precision": 1.0,
        "recall": 1.0,
        "f1_score": 1.0,
        "support": 3
      },
      "oncological": {
        "precision": 0.6667,
        "recall": 1.0,
        "f1_score": 0.8,
        "support": 2
      }
    }
  },
  "download_url": "/api/v1/ml/download/predictions_20250825_223034.csv",
  "processing_time": 0.82
}
```

### Métricas del modelo

```json
{
  "f1_score": 0.89,
  "accuracy": 0.92,
  "precision": 0.91,
  "recall": 0.87,
  "total_classes": 15
}
```

## 🛠️ Desarrollo

### Estructura del proyecto

```
techsphere/
├── api/                    # Código de la API
│   ├── controllers/        # Controladores HTTP
│   ├── services/          # Servicios de negocio
│   ├── models/            # Modelos de datos
│   ├── core/              # Configuración
│   └── main.py           # Aplicación principal
├── scibert_classifier/    # Modelo ML entrenado
├── main.py               # Script original del modelo
├── run_api.py           # Script para ejecutar API
└── requirements.txt     # Dependencias
```

### Agregar nuevas funcionalidades

1. **Nuevo endpoint**: Agregar en `controllers/`
2. **Nueva lógica de negocio**: Implementar en `services/`
3. **Nuevos modelos de datos**: Definir en `models/schemas.py`
4. **Nueva configuración**: Agregar en `core/config.py`

## 🔒 Producción

Para desplegar en producción:

1. **Configurar variables de entorno**
2. **Usar ASGI server** como Gunicorn + Uvicorn
3. **Configurar CORS** específicamente
4. **Agregar autenticación** si es necesario
5. **Configurar logging** apropiado
6. **Usar base de datos** para persistencia si se requiere

## 📋 Entrega Final

Este proyecto incluye un reporte técnico completo que documenta todo el desarrollo, arquitectura, metodología y resultados obtenidos:

📄 **[Report Tech Sphere Challenge.pdf](./Report%20Tech%20Sphere%20Challenge.pdf)**

El reporte contiene:

- **Análisis del problema** y enfoque de solución
- **Arquitectura técnica** detallada del sistema
- **Metodología de desarrollo** y decisiones de diseño
- **Implementación** de funcionalidades principales
- **Evaluación de resultados** y métricas de rendimiento
- **Conclusiones** y trabajo futuro

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

**TechSphere ML API** - Análisis inteligente de textos científicos 🔬🚀
