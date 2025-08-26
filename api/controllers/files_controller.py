"""
Controlador para manejo de archivos
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import os

from ..core.config import config

router = APIRouter(prefix="/ml", tags=["Files"])

@router.get(
    "/download/{filename}",
    summary="Descargar archivo procesado",
    description="Descarga un archivo CSV procesado de predicciones batch"
)
async def download_processed_file(filename: str):
    """
    Descarga un archivo CSV procesado.
    
    - **filename**: Nombre del archivo a descargar
    
    Retorna el archivo CSV con las predicciones procesadas.
    """
    try:
        # Validar nombre de archivo (seguridad)
        if not filename.endswith('.csv') or '..' in filename or '/' in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nombre de archivo inválido"
            )
        
        # Buscar archivo en directorio temporal
        temp_dir = Path(config.get_project_root()) / "temp"
        file_path = temp_dir / filename
        
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo no encontrado"
            )
        
        # Verificar que el archivo no sea muy antiguo (opcional)
        file_age = os.path.getctime(file_path)
        import time
        if time.time() - file_age > 3600:  # 1 hora
            # Opcional: eliminar archivos antiguos
            file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo expirado"
            )
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="text/csv"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error descargando archivo: {str(e)}"
        )
