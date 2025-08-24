# TechSphere ML API

API para análisis de textos científicos utilizando SciBERT con arquitectura por capas.

## 🚀 Características

- **Clasificación de textos científicos** con modelo SciBERT entrenado
- **Dashboard interactivo** con métricas principales (F1-score, Accuracy)
- **Matriz de confusión visual** para análisis de rendimiento
- **Gráficos de distribución** de clases médicas
- **Demo funcional** para probar clasificaciones en tiempo real
- **Visualización de características** más importantes del modelo

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
   # techsphere-env\Scripts\activate

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

```bash
# Opción 1: Usando el script
python run_api.py

# Opción 2: Usando uvicorn directamente
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://localhost:8000`

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

- `POST /api/v1/ml/predict` - Clasificar texto científico
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

### Clasificar texto científico

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hypothesis: ACE inhibitors improves heart disease outcomes via acute myeloid leukemia pathways. Methods: randomized controlled trial with 264 diabetic patients, measuring interstitial nephritis and kidney. Results: better quality of life measures. Conclusion: cost-effectiveness implications."
     }'
```

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

### Predicción

```json
{
  "predicted_class": "cardiovascular|neurological",
  "confidence": 0.87,
  "probabilities": {
    "cardiovascular": 0.45,
    "neurological": 0.42,
    "oncological": 0.13
  },
  "categories": ["cardiovascular", "neurological"]
}
```

### Métricas

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
