from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.models.compuesto import Compuesto
from app.repositories.compuesto_repo import CompuestoRepository
from app.repositories.compuesto_por_medicamento_repo import CompuestoPorMedicamentoRepository

class CompuestoService:
    """Service class for Compuesto business logic"""
    
    @staticmethod
    async def get_all_compuestos() -> List[Compuesto]:
        """Get all compuestos"""
        return await CompuestoRepository.get_all()
    
    @staticmethod
    async def get_compuesto_by_id(compuesto_id: str) -> Compuesto:
        """Get a compuesto by ID with validation"""
        compuesto = await CompuestoRepository.get_by_id(compuesto_id)
        if not compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        return compuesto
    
    @staticmethod
    async def create_compuesto(compuesto: Compuesto) -> Compuesto:
        """Create a new compuesto with validation"""
        if not compuesto.nombre or compuesto.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compuesto name cannot be empty"
            )
        
        return await CompuestoRepository.create(compuesto)
    
    @staticmethod
    async def update_compuesto(compuesto_id: str, compuesto: Compuesto) -> Compuesto:
        """Update an existing compuesto with validation"""
        existing_compuesto = await CompuestoRepository.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        
        if not compuesto.nombre or compuesto.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compuesto name cannot be empty"
            )
        
        return await CompuestoRepository.update(compuesto_id, compuesto)
    
    @staticmethod
    async def delete_compuesto(compuesto_id: str) -> Dict[str, Any]:
        """Delete a compuesto with validation and cascade deletion"""
        existing_compuesto = await CompuestoRepository.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        
        # borrrar las relaciones con medicamentos
        deleted_relations = await CompuestoPorMedicamentoRepository.delete_by_compuesto_id(compuesto_id)
        
        # borrar el compuesto
        result = await CompuestoRepository.delete(compuesto_id)
        
        return {
            "deleted": result,
            "id": compuesto_id,
            "related_records_deleted": deleted_relations
        }
    
    @staticmethod
    async def get_medicamentos_by_compuesto(compuesto_id: str) -> List[Dict[str, Any]]:
        """Get all medicamentos that contain this compuesto"""
        # verificar que el compuesto existe
        existing_compuesto = await CompuestoRepository.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        
        return await CompuestoRepository.get_medicamentos_by_compuesto_id(compuesto_id)