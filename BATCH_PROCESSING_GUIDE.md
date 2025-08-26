# 📊 Guía de Procesamiento Batch - TechSphere ML API

## 🎯 Introducción

La funcionalidad de **procesamiento batch** permite evaluar el rendimiento del modelo SciBERT procesando múltiples textos científicos desde un archivo CSV, obteniendo predicciones y métricas de evaluación automáticamente.

## 📋 Requisitos del Archivo CSV

### Columnas Requeridas

El archivo CSV debe contener exactamente estas columnas:

| Columna    | Descripción                              | Ejemplo                                           |
| ---------- | ---------------------------------------- | ------------------------------------------------- |
| `title`    | Título del artículo científico           | "Mechanisms of myocardial ischemia"               |
| `abstract` | Resumen/abstract del artículo            | "The role of epinephrine in eliciting..."         |
| `group`    | Categorías reales (etiquetas verdaderas) | "cardiovascular" o "cardiovascular\|neurological" |

### Formato de Categorías

- **Single label**: `"cardiovascular"`, `"neurological"`, `"oncological"`, `"hepatorenal"`
- **Multi label**: `"cardiovascular|neurological"`, `"hepatorenal|oncological"`

## 📁 Ejemplos de Archivos CSV

### Ejemplo 1: Dataset Básico

```csv
title,abstract,group
"Mechanisms of myocardial ischemia induced by epinephrine","The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease. Objective signs of ischemia and factors increasing myocardial oxygen consumption were compared.","cardiovascular"
"Brain tumor classification using convolutional neural networks","Deep learning approaches have shown promising results in medical image analysis particularly for brain tumor detection and classification. We developed a CNN-based model for automatic brain tumor classification from MRI scans.","neurological"
"Hepatocellular carcinoma treatment outcomes with sorafenib therapy","This retrospective study analyzed treatment outcomes in patients with advanced hepatocellular carcinoma receiving sorafenib therapy. We evaluated overall survival and adverse events.","hepatorenal|oncological"
```

### Ejemplo 2: Dataset Multilabel Complejo

```csv
title,abstract,group
"Cardiovascular risk factors in diabetic patients with chronic kidney disease","This cross-sectional study examined cardiovascular risk factors in diabetic patients with various stages of chronic kidney disease. We assessed the relationship between kidney function and cardiovascular outcomes.","cardiovascular|hepatorenal"
"Neurological complications following cardiac surgery","We conducted a systematic review of neurological complications occurring after cardiac surgical procedures including stroke, delirium and cognitive dysfunction.","cardiovascular|neurological"
"Liver metastases from colorectal cancer: surgical management","This study evaluated surgical outcomes in patients with colorectal liver metastases undergoing hepatic resection. We analyzed factors associated with survival and recurrence patterns.","hepatorenal|oncological"
```

## 🚀 Cómo Usar la Funcionalidad

### Paso 1: Preparar el Archivo

1. Crear un archivo CSV con las columnas requeridas
2. Asegurarse de que los títulos y abstracts estén bien formateados
3. Verificar que las categorías usen el formato correcto (`|` para multilabel)

### Paso 2: Enviar Solicitud

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict-batch" \
     -H "accept: application/json" \
     -F "file=@your_dataset.csv" \
     -F "threshold=0.4"
```

**Parámetros:**

- `file`: Archivo CSV a procesar
- `threshold`: Umbral para clasificación multilabel (0.0-1.0)

### Paso 3: Analizar Respuesta

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
      }
    }
  },
  "download_url": "/api/v1/ml/download/predictions_20250825_223034.csv",
  "processing_time": 0.82
}
```

### Paso 4: Descargar Resultados

```bash
curl -X GET "http://localhost:8000/api/v1/ml/download/predictions_20250825_223034.csv" \
     --output processed_results.csv
```

## 📊 Interpretación de Métricas

### Métricas Generales

- **Accuracy**: Rendimiento general del modelo (0.0-1.0)
- **Precision**: Proporción de predicciones positivas correctas
- **Recall**: Proporción de casos positivos identificados correctamente
- **F1-Score**: Media armónica entre precision y recall

### Métricas Multilabel Específicas

- **Hamming Loss**: Fracción de etiquetas incorrectamente predichas (menor es mejor)
- **Exact Match Ratio**: Porcentaje de muestras donde todas las etiquetas coinciden exactamente

### Métricas por Categoría

```json
"category_metrics": {
  "cardiovascular": {
    "precision": 1.0,      // Sin falsos positivos
    "recall": 0.6667,      // 67% de casos detectados
    "f1_score": 0.8,       // Balance precision-recall
    "support": 3           // 3 muestras reales de esta categoría
  }
}
```

## 📄 Archivo de Salida

El archivo procesado incluye:

```csv
title,abstract,group,group_predicted,confidence,combined_text
"Mechanisms of myocardial ischemia","The role of epinephrine...","cardiovascular","cardiovascular",0.9939,"Mechanisms of myocardial ischemia The role of epinephrine..."
```

**Columnas añadidas:**

- `group_predicted`: Categorías predichas por el modelo
- `confidence`: Nivel de confianza (0.0-1.0)
- `combined_text`: Texto concatenado usado para predicción

## 🎯 Casos de Uso

### 1. Evaluación de Rendimiento

- Subir dataset de prueba con etiquetas conocidas
- Obtener métricas detalladas del modelo
- Identificar categorías con menor rendimiento

### 2. Clasificación Masiva

- Procesar grandes volúmenes de artículos científicos
- Obtener clasificaciones automáticas
- Descargar resultados para análisis posterior

### 3. Ajuste de Umbral

- Probar diferentes valores de threshold (0.1-0.9)
- Encontrar el balance óptimo precision-recall
- Optimizar para casos de uso específicos

## ⚠️ Limitaciones y Consideraciones

- **Tamaño de archivo**: Recomendado < 1000 registros por batch
- **Tiempo de procesamiento**: ~0.1-0.2 segundos por registro
- **Formato requerido**: CSV con codificación UTF-8
- **Archivos temporales**: Se eliminan automáticamente después de 1 hora
- **Memoria**: El procesamiento se hace registro por registro para eficiencia

## 🔧 Resolución de Problemas

### Error: "Columnas faltantes en el CSV"

**Solución**: Verificar que el CSV contenga exactamente: `title`, `abstract`, `group`

### Error: "El archivo debe ser un CSV"

**Solución**: Asegurar que el archivo tenga extensión `.csv`

### Error: "El archivo CSV está vacío"

**Solución**: Verificar que el CSV contenga al menos una fila de datos (además del header)

### Error: "Archivo no encontrado" (al descargar)

**Solución**: El archivo puede haber expirado (1 hora). Re-ejecutar el procesamiento.

## 💡 Tips y Mejores Prácticas

1. **Preparación de datos**: Limpiar títulos y abstracts de caracteres especiales
2. **Tamaño de batch**: Para archivos grandes, dividir en lotes de ~500 registros
3. **Umbral óptimo**: Comenzar con 0.5 y ajustar según resultados
4. **Formato multilabel**: Usar exactamente `|` para separar categorías
5. **Validación**: Revisar sample_data.csv como referencia de formato correcto
