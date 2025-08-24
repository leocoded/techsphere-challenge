#!/usr/bin/env python3
"""
Script para ejecutar la API de TechSphere
"""
import uvicorn
from api.main import app

if __name__ == "__main__":
    print("🚀 Iniciando TechSphere ML API...")
    print("📖 Documentación disponible en: http://localhost:8000/api/v1/docs")
    print("🔍 Redoc disponible en: http://localhost:8000/api/v1/redoc")
    print("💡 Health check en: http://localhost:8000/api/v1/health")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
