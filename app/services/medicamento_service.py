from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.models.medicamento import medicamento
from app.models.compuesto_med import compuesto_med
from app.repositories.medicamentos_repo import medicamentos_repo
from app.repositories.compuesto_por_medicamento_repo import compuesto_por_medicamento_repo
from app.repositories.compuesto_repo import compuesto_repo

class MedicamentoService:
    """Service class for medicamento business logic"""
    
    @staticmethod
    async def get_all_medicamentos() -> List[medicamento]:
        """Get all medicamentos"""
        return await medicamentos_repo.get_all()
    
    @staticmethod
    async def get_medicamento_by_id(medicamento_id: str) -> medicamento:
        """Get a medicamento by ID with validation"""
        medicamento = await medicamentos_repo.get_by_id(medicamento_id)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"medicamento with ID {medicamento_id} not found"
            )
        return medicamento
    
    @staticmethod
    async def create_medicamento(medicamento: medicamento) -> medicamento:
        """Create a new medicamento with validation"""
        #validacion que nombre y fabricante no estan vacios
        if not medicamento.nombre or medicamento.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="medicamento name cannot be empty"
            )
        
        if not medicamento.fabricante or medicamento.fabricante.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fabricante cannot be empty"
            )
        
        return await medicamentos_repo.create(medicamento)
    
    @staticmethod
    async def update_medicamento(medicamento_id: str, medicamento: medicamento) -> medicamento:
        """Update an existing medicamento with validation"""
        existing_medicamento = await medicamentos_repo.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"medicamento with ID {medicamento_id} not found"
            )
        
        #validacion que nombre y fabricante no estan vacios
        if not medicamento.nombre or medicamento.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="medicamento name cannot be empty"
            )
        
        if not medicamento.fabricante or medicamento.fabricante.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fabricante cannot be empty"
            )
        
        return await medicamentos_repo.update(medicamento_id, medicamento)
    
    @staticmethod
    async def delete_medicamento(medicamento_id: str) -> Dict[str, Any]:
        """Delete a medicamento with validation and cascade deletion"""
        existing_medicamento = await medicamentos_repo.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"medicamento with ID {medicamento_id} not found"
            )
        
        # Delete associated relations first (cascade delete)
        deleted_relations = await compuesto_por_medicamento_repo.delete_by_medicamento_id(medicamento_id)
        
        # Delete the medicamento
        result = await medicamentos_repo.delete(medicamento_id)
        
        return {
            "deleted": result,
            "id": medicamento_id,
            "related_records_deleted": deleted_relations
        }
    
    @staticmethod
    async def get_compuestos_by_medicamento(medicamento_id: str) -> List[Dict[str, Any]]:
        """Get all compuestos that are in this medicamento"""
        existing_medicamento = await medicamentos_repo.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"medicamento with ID {medicamento_id} not found"
            )
        
        return await medicamentos_repo.get_compuestos_by_medicamento_id(medicamento_id)
    
    @staticmethod
    async def add_compuesto_to_medicamento(
        medicamento_id: str, 
        compuesto_id: str, 
        concentracion: float, 
        unidad: str
    ) -> compuesto_med:
        """Add a compuesto to a medicamento with validation"""
        existing_medicamento = await medicamentos_repo.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"medicamento with ID {medicamento_id} not found"
            )
        
        existing_compuesto = await compuesto_repo.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        
        # Validacion de concentracion
        if concentracion <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Concentration must be greater than zero"
            )
        
        # Validacion de unidad
        if not unidad or unidad.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit of measure cannot be empty"
            )
        
        compuesto_med_data = {
            "medicamento_id": medicamento_id,
            "compuesto_id": compuesto_id,
            "concentracion": concentracion,
            "unidad_medida": unidad
        }
        
        return await compuesto_por_medicamento_repo.create(compuesto_med_data)