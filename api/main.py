"""
TechSphere ML API - API para análisis de textos científicos con SciBERT
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .core.config import config
from .controllers import ml_controller, analytics_controller, system_controller, files_controller

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=config.APP_NAME,
    description="""
    API para análisis de textos científicos utilizando SciBERT.
    
    ## Características principales:
    
    * **Clasificación de textos individual**: Clasifica textos científicos en categorías médicas
    * **🆕 Procesamiento batch desde CSV**: Carga archivos CSV para clasificación masiva y evaluación
    * **🆕 Métricas multilabel avanzadas**: Hamming Loss, Exact Match Ratio, métricas por categoría
    * **🆕 Descarga de resultados**: Archivos CSV procesados con predicciones
    * **Métricas del modelo**: Obtiene F1-score, accuracy, precision y recall con datos reales
    * **Análisis visual**: Matriz de confusión, distribución de clases, importancia de características
    * **Demo funcional**: Endpoint para probar clasificaciones en tiempo real
    * **Dashboard datos**: Endpoints para crear visualizaciones interactivas
    * **🆕 Umbral configurable**: Ajuste de sensibilidad para clasificación multilabel
    
    ## Categorías de clasificación:
    
    El modelo puede clasificar textos en las siguientes categorías médicas:
    - **Cardiovascular**: Estudios relacionados con el sistema cardiovascular
    - **Neurological**: Investigaciones sobre el sistema nervioso
    - **Oncological**: Estudios relacionados con el cáncer
    - **Hepatorenal**: Investigaciones sobre hígado y riñones
    
    También puede identificar combinaciones de categorías (clasificación multilabel).
    
    ## 🆕 Funcionalidad Batch:
    
    ### Formato CSV requerido:
    ```csv
    title,abstract,group
    "Título del artículo","Resumen del artículo","cardiovascular|neurological"
    ```
    
    ### Proceso:
    1. **Subir CSV** → POST `/api/v1/ml/predict-batch`
    2. **Obtener métricas** → Accuracy, Precision, Recall, F1, Hamming Loss
    3. **Descargar resultados** → GET `/api/v1/ml/download/{filename}`
    
    ### Métricas calculadas:
    - Rendimiento general (Accuracy, F1-Score)
    - Métricas multilabel (Hamming Loss, Exact Match Ratio)  
    - Métricas por categoría individual
    - Tiempo de procesamiento
    """,
    version=config.APP_VERSION,
    docs_url=f"{config.API_PREFIX}/docs",
    redoc_url=f"{config.API_PREFIX}/redoc",
    openapi_url=f"{config.API_PREFIX}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(system_controller.router, prefix=config.API_PREFIX)
app.include_router(ml_controller.router, prefix=config.API_PREFIX)
app.include_router(analytics_controller.router, prefix=config.API_PREFIX)
app.include_router(files_controller.router, prefix=config.API_PREFIX)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = request.state.start_time = request.headers.get("x-start-time")
    
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"Response: {response.status_code}")
    
    return response

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": "Ha ocurrido un error inesperado",
            "timestamp": request.state.start_time
        }
    )

# Endpoint raíz
@app.get("/", include_in_schema=False)
async def root():
    """Endpoint raíz que redirige a la documentación"""
    return {
        "message": f"Bienvenido a {config.APP_NAME}",
        "version": config.APP_VERSION,
        "docs": f"{config.API_PREFIX}/docs",
        "redoc": f"{config.API_PREFIX}/redoc"
    }

# Customizar OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=config.APP_NAME,
        version=config.APP_VERSION,
        description=app.description,
        routes=app.routes,
    )
    
    # Personalizar schema
    openapi_schema["info"]["x-logo"] = {
        "url": "https://via.placeholder.com/150x50/1f77b4/ffffff?text=TechSphere"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
