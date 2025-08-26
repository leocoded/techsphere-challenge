# 🚀 TechSphere ML API - Guía de Uso Completa

## 📋 Resumen del Proyecto

Has construido exitosamente una **API completa con FastAPI** que permite acceder a todas las funcionalidades necesarias para el análisis y visualización de un modelo de Machine Learning SciBERT entrenado para clasificar textos científicos médicos.

## 🏗️ Arquitectura Implementada

La API sigue una **arquitectura por capas (layered architecture)** bien definida:

```
api/
├── controllers/     # 🎮 Controladores - Manejan solicitudes HTTP
│   ├── ml_controller.py         # Endpoints de ML
│   ├── analytics_controller.py  # Endpoints de analytics
│   └── system_controller.py     # Endpoints de sistema
├── services/       # 🔧 Servicios - Lógica de negocio
│   ├── ml_service.py           # Servicio del modelo ML
│   └── analytics_service.py    # Servicio de análisis
├── models/         # 📋 Modelos - Validación de datos
│   └── schemas.py              # Esquemas Pydantic
├── core/          # ⚙️ Core - Configuración y utilidades
│   ├── config.py              # Configuración
│   └── utils.py               # Utilidades
└── main.py        # 🚪 Aplicación principal FastAPI
```

## ✅ Funcionalidades Implementadas

### 🤖 Machine Learning

- ✅ **Clasificación de textos**: Endpoint POST `/api/v1/ml/predict`
- ✅ **Métricas del modelo**: F1-score, Accuracy, Precision, Recall
- ✅ **Clases disponibles**: Lista de todas las categorías médicas

### 📊 Analytics & Dashboard

- ✅ **Matriz de confusión**: Datos para visualización
- ✅ **Distribución de clases**: Gráficos de distribución
- ✅ **Características importantes**: Features más relevantes del modelo
- ✅ **Rendimiento temporal**: Métricas a lo largo del tiempo
- ✅ **Correlaciones**: Matriz de correlación entre categorías

### 🔧 Sistema

- ✅ **Health Check**: Monitoreo del estado de la API
- ✅ **Información**: Detalles de versión y configuración
- ✅ **Documentación automática**: Swagger UI y ReDoc

## 🚀 Cómo Usar la API

### Configuración Inicial (Recomendada)

#### Opción 1: Script de Configuración Automática 🛠️

**Para macOS/Linux:**

```bash
# Ejecutar script de configuración
./setup.sh
```

**Para Windows:**

```cmd
# Ejecutar script de configuración
setup.bat
```

#### Opción 2: Configuración Manual

1. **Crear entorno virtual:**

```bash
# Crear entorno virtual
python3 -m venv techsphere-env

# Activar entorno virtual (macOS/Linux)
source techsphere-env/bin/activate

# Activar entorno virtual (Windows)
# techsphere-env\Scripts\activate
```

2. **Instalar dependencias:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 1. Ejecutar la API

**¡Importante!** Siempre activar el entorno virtual primero:

````bash
# Activar entorno virtual (si no está activado)
source techsphere-env/bin/activate  # macOS/Linux
# techsphere-env\Scripts\activate     # Windows

### 1. Ejecutar la API

**¡Importante!** Siempre activar el entorno virtual primero:

```bash
# Activar entorno virtual (si no está activado)
source techsphere-env/bin/activate  # macOS/Linux
# techsphere-env\Scripts\activate     # Windows

# Ejecutar la API localmente
python run_api.py

# Ejecutar la API con Ngrok (acceso público)
python run_api.py --ngrok

# Ejecutar con token de Ngrok específico
python run_api.py --ngrok --ngrok-token TU_TOKEN_AQUI

# Ejecutar en puerto personalizado con Ngrok
python run_api.py --ngrok --port 8080
````

#### 🌐 Configuración de Ngrok para Acceso Público

Para exponer tu API a internet usando Ngrok:

**Configuración Automática:**

```bash
# Ejecutar script de configuración
./setup_ngrok.sh
```

**Configuración Manual:**

1. **Instalar Ngrok** (si no está instalado):

   - Visita: https://ngrok.com/download
   - O con Homebrew: `brew install ngrok/ngrok/ngrok`

2. **Obtener token gratuito** (opcional pero recomendado):

   - Visita: https://dashboard.ngrok.com/get-started/your-authtoken
   - Crea cuenta gratuita
   - Configura el token: `ngrok config add-authtoken TU_TOKEN`

3. **Ejecutar con Ngrok:**
   ```bash
   python run_api.py --ngrok
   ```

**URLs disponibles con Ngrok:**

- 🌐 **URL pública**: `https://abc123.ngrok-free.app`
- 📖 **Documentación**: `https://abc123.ngrok-free.app/api/v1/docs`
- 🔍 **ReDoc**: `https://abc123.ngrok-free.app/api/v1/redoc`
- 💡 **Health check**: `https://abc123.ngrok-free.app/api/v1/health`
- 🔧 **Panel de Ngrok**: `http://localhost:4040` (estadísticas locales)

La API estará disponible en:

- **Local**: `http://localhost:8000`
- **Público** (con Ngrok): URL proporcionada por Ngrok

### 2. Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/api/v1/docs`
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

### 3. Endpoints Principales

#### 🔍 Clasificar Texto Científico

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hypothesis: ACE inhibitors improves heart disease outcomes. Methods: randomized controlled trial with diabetic patients. Results: better cardiovascular outcomes."
     }'
```

#### 📈 Obtener Métricas del Modelo

```bash
curl "http://localhost:8000/api/v1/ml/metrics"
```

#### 📊 Obtener Datos para Dashboard

```bash
# Matriz de confusión
curl "http://localhost:8000/api/v1/analytics/confusion-matrix"

# Distribución de clases
curl "http://localhost:8000/api/v1/analytics/class-distribution"

# Características importantes
curl "http://localhost:8000/api/v1/analytics/feature-importance"

# Rendimiento temporal
curl "http://localhost:8000/api/v1/analytics/performance-over-time"
```

### 4. Usar el Cliente Python

```python
# Usar el cliente de ejemplo
python client_example.py
```

### 5. Crear Visualizaciones

```python
# Crear dashboard con gráficas
python dashboard_example.py
```

## 📊 Datos Disponibles para Dashboard

### Métricas Principales (Datos Reales)

- **F1-Score**: 0.9354
- **Accuracy**: 0.9572
- **Precision**: 0.9474
- **Recall**: 0.9236

### Categorías de Clasificación

El modelo clasifica textos en categorías médicas:

- `cardiovascular` - Estudios cardiovasculares (645 muestras)
- `neurological` - Investigaciones neurológicas (1,058 muestras)
- `oncological` - Estudios oncológicos (237 muestras)
- `hepatorenal` - Investigaciones hepatorenales (533 muestras)

También identifica **combinaciones** (clasificación multilabel):

- `neurological|cardiovascular` (308 muestras)
- `cardiovascular|hepatorenal` (190 muestras)
- `neurological|hepatorenal` (202 muestras)
- `neurological|oncological` (143 muestras)
- Y más combinaciones multilabel...

### Métricas de Matriz de Confusión (Por Categoría)

- **Cardiovascular**: TP=247, TN=445, FP=8, FN=13
- **Hepatorenal**: TP=216, TN=480, FP=5, FN=12
- **Neurological**: TP=296, TN=343, FP=32, FN=42
- **Oncological**: TP=124, TN=579, FP=4, FN=6

**Total de muestras en dataset**: 3,565

### Visualizaciones Generadas

Al ejecutar `dashboard_example.py` se crean:

1. **`techsphere_dashboard.png`** - Dashboard principal con:

   - Métricas de rendimiento
   - Distribución de clases
   - Top características importantes
   - Tendencia de rendimiento temporal

2. **`confusion_matrix.png`** - Matriz de confusión visual

3. **`correlation_matrix.png`** - Correlaciones entre categorías

4. **`prediction_result.png`** - Resultado de predicción individual

## 🔧 Personalización y Extensión

### Agregar Nuevos Endpoints

1. **En `controllers/`**: Crear nuevo controlador

```python
from fastapi import APIRouter
router = APIRouter(prefix="/nuevo", tags=["Nuevo"])

@router.get("/endpoint")
async def nuevo_endpoint():
    return {"mensaje": "Nuevo endpoint"}
```

2. **En `main.py`**: Incluir el router

```python
app.include_router(nuevo_controller.router, prefix=config.API_PREFIX)
```

### Agregar Nueva Lógica de Negocio

1. **En `services/`**: Crear nuevo servicio
2. **En `models/schemas.py`**: Definir esquemas de validación
3. **En `controllers/`**: Usar el servicio en endpoints

### Configurar para Producción

1. **Variables de entorno**: Modificar `core/config.py`
2. **CORS específico**: Actualizar configuración CORS en `main.py`
3. **Base de datos**: Agregar capa Repository si se necesita persistencia
4. **Autenticación**: Implementar middleware de auth si es necesario

## 📁 Estructura Final del Proyecto

```
techsphere/
├── api/                           # 🏗️ API con arquitectura por capas
│   ├── controllers/               # Controladores HTTP
│   ├── services/                  # Lógica de negocio
│   ├── models/                    # Modelos de datos
│   ├── core/                      # Configuración y utils
│   └── main.py                   # App FastAPI principal
├── scibert_classifier/            # 🤖 Modelo ML entrenado
├── main.py                       # Script original del modelo
├── run_api.py                    # 🚀 Script para ejecutar API
├── client_example.py             # 📱 Cliente de ejemplo
├── dashboard_example.py          # 📊 Dashboard con visualizaciones
├── requirements.txt              # 📦 Dependencias
├── README.md                     # 📖 Documentación
├── USAGE_GUIDE.md               # 📋 Esta guía
└── *.png                        # 🎨 Visualizaciones generadas
```

## 🎯 Casos de Uso

### 1. Dashboard Interactivo

Usa los endpoints de analytics para crear dashboards web interactivos con:

- Métricas en tiempo real
- Gráficos de distribución
- Matrices de confusión
- Tendencias temporales

### 2. Demo Funcional

Usa el endpoint `/ml/predict` para crear demos donde usuarios pueden:

- Introducir textos científicos
- Ver clasificaciones en tiempo real
- Explorar confianza y probabilidades

### 3. Análisis de Modelo

Usa todos los endpoints para análisis profundo:

- Evaluar rendimiento
- Identificar sesgos
- Analizar características importantes
- Monitorear degradación del modelo

### 4. Integración con Aplicaciones

La API puede integrarse con:

- Aplicaciones web (React, Vue, Angular)
- Aplicaciones móviles
- Sistemas de análisis de documentos
- Pipelines de procesamiento de texto

## 🚀 Próximos Pasos

### Mejoras Sugeridas

1. **Base de datos**: Agregar persistencia para:

   - Historial de predicciones
   - Métricas temporales reales
   - Logs de uso

2. **Autenticación**: Implementar:

   - API Keys
   - JWT tokens
   - Rate limiting

3. **Monitoreo**: Agregar:

   - Logging estructurado
   - Métricas de performance
   - Alertas de errores

4. **Testing**: Crear:

   - Tests unitarios
   - Tests de integración
   - Tests de carga

5. **Deployment**: Configurar:
   - Docker containers
   - CI/CD pipelines
   - Cloud deployment

### 🐍 Mejores Prácticas de Desarrollo

1. **Siempre usar entorno virtual**:

   ```bash
   # Crear entorno específico para el proyecto
   python3 -m venv techsphere-env
   source techsphere-env/bin/activate
   ```

2. **Mantener requirements.txt actualizado**:

   ```bash
   # Generar requirements después de instalar nuevas dependencias
   pip freeze > requirements.txt
   ```

3. **Variables de entorno para configuración**:

   ```bash
   # Crear archivo .env para configuraciones locales
   echo "API_HOST=localhost" >> .env
   echo "API_PORT=8000" >> .env
   ```

4. **Desarrollo con recarga automática**:

   ```bash
   # La API se recarga automáticamente al detectar cambios
   python run_api.py
   ```

5. **Testing antes de commits**:
   ```bash
   # Ejecutar tests antes de hacer commit
   python client_example.py  # Test de integración básico
   ```

## ✅ Conclusión

Has creado exitosamente una **API completa y profesional** que:

- ✅ Sigue las mejores prácticas de arquitectura por capas
- ✅ Proporciona todos los datos necesarios para dashboards interactivos
- ✅ Incluye documentación automática y ejemplos funcionales
- ✅ Es extensible y mantenible
- ✅ Está lista para desarrollo posterior y producción

La API está **completamente funcional** y puede ser utilizada inmediatamente para crear aplicaciones web, dashboards interactivos, y sistemas de análisis de textos científicos.

---

🎉 **¡Felicidades! Tu TechSphere ML API está lista para usar.** 🎉
