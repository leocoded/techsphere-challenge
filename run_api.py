#!/usr/bin/env python3
"""
Script para ejecutar la API de TechSphere con soporte para Ngrok
"""
import uvicorn
import argparse
import sys
import signal
import atexit
from api.main import app
from ngrok_config import setup_ngrok, cleanup_ngrok, get_ngrok_auth_token

# Variable global para almacenar la URL de Ngrok
ngrok_url = None

def signal_handler(sig, frame):
    """Maneja las señales de interrupción para cerrar Ngrok correctamente"""
    print("\n🛑 Cerrando servidor...")
    cleanup_ngrok()
    sys.exit(0)

def parse_arguments():
    """Parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description="TechSphere ML API Server")
    parser.add_argument(
        "--ngrok", 
        action="store_true", 
        help="Exponer la API a través de Ngrok"
    )
    parser.add_argument(
        "--ngrok-token",
        type=str,
        help="Token de autenticación de Ngrok (opcional)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Puerto para el servidor (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host para el servidor (default: 0.0.0.0)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    # Parsear argumentos
    args = parse_arguments()
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_ngrok)
    
    print("🚀 Iniciando TechSphere ML API...")
    
    # Configurar Ngrok si se solicita
    if args.ngrok:
        print("🌐 Configurando Ngrok...")
        auth_token = args.ngrok_token or get_ngrok_auth_token()
        ngrok_url = setup_ngrok(port=args.port, auth_token=auth_token)
        
        if not ngrok_url:
            print("❌ No se pudo configurar Ngrok. Ejecutando solo localmente.")
            args.ngrok = False
    
    # Mostrar información de acceso local
    if not args.ngrok:
        print(f"📖 Documentación disponible en: http://localhost:{args.port}/api/v1/docs")
        print(f"🔍 Redoc disponible en: http://localhost:{args.port}/api/v1/redoc")
        print(f"💡 Health check en: http://localhost:{args.port}/api/v1/health")
    
    # Ejecutar el servidor
    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        reload=True,
        log_level="info",
        access_log=True
    )
