"""
Configuración de Ngrok para TechSphere API
"""
import os
from pyngrok import ngrok
import logging

logger = logging.getLogger(__name__)

def setup_ngrok(port=8000, auth_token=None):
    """
    Configura Ngrok para exponer la API a la web
    
    Args:
        port (int): Puerto donde corre la API (default: 8000)
        auth_token (str): Token de autenticación de Ngrok (opcional)
    
    Returns:
        str: URL pública de Ngrok
    """
    try:
        # Si se proporciona un token de autenticación, configurarlo
        if auth_token:
            ngrok.set_auth_token(auth_token)
            logger.info("✅ Token de Ngrok configurado")
        
        # Crear túnel HTTP
        public_url = ngrok.connect(port, "http")
        logger.info(f"🌐 Ngrok túnel creado: {public_url}")
        
        # Mostrar información útil
        print(f"\n🚀 TechSphere API está disponible públicamente en:")
        print(f"   📡 URL pública: {public_url}")
        print(f"   📖 Documentación: {public_url}/api/v1/docs")
        print(f"   🔍 Redoc: {public_url}/api/v1/redoc")
        print(f"   💡 Health check: {public_url}/api/v1/health")
        print(f"\n🔧 Panel de Ngrok: http://localhost:4040")
        print("   (Para ver estadísticas y logs del túnel)\n")
        
        return public_url
        
    except Exception as e:
        logger.error(f"❌ Error configurando Ngrok: {str(e)}")
        print(f"❌ Error configurando Ngrok: {str(e)}")
        print("💡 Posibles soluciones:")
        print("   1. Instala Ngrok: https://ngrok.com/download")
        print("   2. Crea una cuenta gratuita en https://ngrok.com/")
        print("   3. Configura tu token: ngrok config add-authtoken <tu-token>")
        return None

def get_ngrok_auth_token():
    """
    Obtiene el token de autenticación de Ngrok desde variables de entorno
    
    Returns:
        str: Token de autenticación o None
    """
    return os.getenv("NGROK_AUTH_TOKEN")

def cleanup_ngrok():
    """
    Limpia los túneles de Ngrok al finalizar
    """
    try:
        ngrok.disconnect()
        ngrok.kill()
        logger.info("🧹 Túneles de Ngrok cerrados correctamente")
    except Exception as e:
        logger.warning(f"⚠️  Error cerrando túneles de Ngrok: {str(e)}")
