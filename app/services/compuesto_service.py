from typing import List, Dict, Optional, Any
from fastapi import HTTPException, status
from app.models.compuesto import compuesto
from app.repositories.compuesto_repo import compuesto_repo
from app.repositories.compuesto_por_medicamento_repo import compuesto_por_medicamento_repo

class CompuestoService:
    """"Clase de servicio para manejar la lógica de negocio relacionada con los compuestos."""

    @staticmethod
    async def get_all_compuestos() -> List[compuesto]:
        """Obtiene todos los compuestos de la base de datos."""
        return await compuesto_repo.get_all_compuestos()

    @staticmethod
    async def get_compuesto_by_id(compuesto_id:str) -> compuesto:
        """Obtiene un compuesto por su ID."""
        compuesto = await compuesto_repo.get_by_id(compuesto_id)
        if not compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto con ID {compuesto_id} no encontrado"
            )
        return compuesto
    
    @staticmethod
    async def create_compuesto(compuesto: compuesto) -> compuesto:
        """Crea un nuevo compuesto en la base de datos."""
        #validar que el nombre no es vacio
        if not compuesto.nombre or compuesto.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del compuesto no puede estar vacío"
            )
        return await compuesto_repo.create(compuesto)
    
    @staticmethod
    async def update_compuesto(compuesto_id: str, compuesto: compuesto) -> compuesto:
        """Actualiza un compuesto existente en la base de datos."""
        #valida que el compuesto existe
        existing_compuesto = await compuesto_repo.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto con ID {compuesto_id} no encontrado"
            )
        

        #valida que el nombre no es vacio
        if not compuesto.nombre or compuesto.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del compuesto no puede estar vacío"
            )
        
        return await compuesto_repo.update(compuesto_id, compuesto)
    
    @staticmethod
    async def delete_compuesto(compuesto_id: str) -> Dict[str,Any]:
        """Elimina un compuesto de la base de datos."""
        #valida que el compuesto existe
        existing_compuesto = await compuesto_repo.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto con ID {compuesto_id} no encontrado"
            )
        
       # borrar las relaciones asociadas primero
        deleted_relations = await compuesto_por_medicamento_repo.delete_by_compuesto_id(compuesto_id)
        
        #borrar el compuesto
        result = await compuesto_repo.delete(compuesto_id)

        return {
            "deleted": result,
            "compuesto_id": compuesto_id,
            "related_records_deleted": deleted_relations
        }
    
    @staticmethod
    async def get_medicamentos_by_compuesto(compuesto_id: str) -> List[Dict[str, Any]]:
        """Get all medicamentos that contain this compuesto"""
        existing_compuesto = await compuesto_repo.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto con ID {compuesto_id} no encontrado"
            )
        
        return await compuesto_repo.get_medicamentos_by_compuesto_id(compuesto_id)