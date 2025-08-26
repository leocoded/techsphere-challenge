"""
Configuración de la aplicación
"""
import os
from pathlib import Path

class Config:
    """Configuración de la aplicación"""
    
    # Rutas del proyecto
    BASE_DIR = Path(__file__).parent.parent.parent
    MODEL_PATH = BASE_DIR / "scibert_classifier"
    
    # Configuración de la API
    API_VERSION = "v1"
    API_PREFIX = f"/api/{API_VERSION}"
    APP_NAME = "TechSphere ML API"
    APP_VERSION = "1.0.0"
    
    # Configuración del modelo
    MAX_TEXT_LENGTH = 512
    
    @classmethod
    def get_model_path(cls) -> str:
        """Obtiene la ruta del modelo"""
        return str(cls.MODEL_PATH)
    
    @classmethod
    def get_project_root(cls) -> Path:
        """Obtiene la ruta raíz del proyecto"""
        return cls.BASE_DIR
    
    @classmethod
    def is_cuda_available(cls) -> bool:
        """Verifica si CUDA está disponible"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

config = Config()
