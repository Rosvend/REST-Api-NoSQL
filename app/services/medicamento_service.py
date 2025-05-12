from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from app.models.medicamento import Medicamento
from app.models.compuesto_med import CompuestoPorMedicamento
from app.repositories.medicamentos_repo import MedicamentoRepository
from app.repositories.compuesto_por_medicamento_repo import CompuestoPorMedicamentoRepository
from app.repositories.compuesto_repo import CompuestoRepository

class MedicamentoService:
    """Service class for Medicamento business logic"""
    
    @staticmethod
    async def get_all_medicamentos() -> List[Medicamento]:
        """Get all medicamentos"""
        return await MedicamentoRepository.get_all()
    
    @staticmethod
    async def get_medicamento_by_id(medicamento_id: str) -> Medicamento:
        """Get a medicamento by ID with validation"""
        medicamento = await MedicamentoRepository.get_by_id(medicamento_id)
        if not medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento with ID {medicamento_id} not found"
            )
        return medicamento
    
    @staticmethod
    async def create_medicamento(medicamento: Medicamento) -> Medicamento:
        """Create a new medicamento with validation"""
        if not medicamento.nombre or medicamento.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medicamento name cannot be empty"
            )
        
        if not medicamento.fabricante or medicamento.fabricante.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fabricante cannot be empty"
            )
        
        return await MedicamentoRepository.create(medicamento)
    
    @staticmethod
    async def update_medicamento(medicamento_id: str, medicamento: Medicamento) -> Medicamento:
        """Update an existing medicamento with validation"""
        existing_medicamento = await MedicamentoRepository.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento with ID {medicamento_id} not found"
            )
        
        if not medicamento.nombre or medicamento.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medicamento name cannot be empty"
            )
        
        if not medicamento.fabricante or medicamento.fabricante.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fabricante cannot be empty"
            )
        
        return await MedicamentoRepository.update(medicamento_id, medicamento)
    
    @staticmethod
    async def delete_medicamento(medicamento_id: str) -> Dict[str, Any]:
        """Delete a medicamento with validation and cascade deletion"""
        existing_medicamento = await MedicamentoRepository.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento with ID {medicamento_id} not found"
            )
        
        # borrar relaciones primero en cascada 
        deleted_relations = await CompuestoPorMedicamentoRepository.delete_by_medicamento_id(medicamento_id)
        
        #borrar medicamento
        result = await MedicamentoRepository.delete(medicamento_id)
        
        return {
            "deleted": result,
            "id": medicamento_id,
            "related_records_deleted": deleted_relations
        }
    
    @staticmethod
    async def get_compuestos_by_medicamento(medicamento_id: str) -> List[Dict[str, Any]]:
        """Get all compuestos that are in this medicamento"""
        existing_medicamento = await MedicamentoRepository.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento with ID {medicamento_id} not found"
            )
        
        return await MedicamentoRepository.get_compuestos_by_medicamento_id(medicamento_id)
    
    @staticmethod
    async def add_compuesto_to_medicamento(
        medicamento_id: str, 
        compuesto_id: str, 
        concentracion: float, 
        unidad: str
    ) -> CompuestoPorMedicamento:
        """Add a compuesto to a medicamento with validation"""
        existing_medicamento = await MedicamentoRepository.get_by_id(medicamento_id)
        if not existing_medicamento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medicamento with ID {medicamento_id} not found"
            )
        
        existing_compuesto = await CompuestoRepository.get_by_id(compuesto_id)
        if not existing_compuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compuesto with ID {compuesto_id} not found"
            )
        
        # validacion de concentracion
        if concentracion <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Concentration must be greater than zero"
            )
        
        # Validacion de unidad de medida
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
        
        return await CompuestoPorMedicamentoRepository.create(compuesto_med_data)