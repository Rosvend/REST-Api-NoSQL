from fastapi import APIRouter, status, Response, Body
from typing import List, Dict, Any
from app.models.medicamento import Medicamento
from app.models.compuesto_med import CompuestoPorMedicamento
from app.services.medicamento_service import MedicamentoService

router = APIRouter(prefix="/api/medicamentos", tags=["medicamentos"])

@router.get("/", response_model=List[Medicamento], status_code=status.HTTP_200_OK)
async def get_all_medicamentos():
    """Endpoint para obtener todos los medicamentos"""
    return await MedicamentoService.get_all_medicamentos()

@router.get("/{medicamento_id}", response_model=Medicamento, status_code=status.HTTP_200_OK)
async def get_medicamento_by_id(medicamento_id: str):
    """Endpoint para obtener un medicamento por su ID"""
    return await MedicamentoService.get_medicamento_by_id(medicamento_id)

@router.get("/{medicamento_id}/compuestos", status_code=status.HTTP_200_OK)
async def get_compuestos_by_medicamento(medicamento_id: str):
    """Endpoint para obtener todos los compuestos de un medicamento"""
    return await MedicamentoService.get_compuestos_by_medicamento(medicamento_id)

@router.post("/", response_model=Medicamento, status_code=status.HTTP_201_CREATED)
async def create_medicamento(medicamento: Medicamento):
    """Endpoint para crear un nuevo medicamento"""
    return await MedicamentoService.create_medicamento(medicamento)

@router.post("/{medicamento_id}/compuestos", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def add_compuesto_to_medicamento(
    medicamento_id: str,
    compuesto_id: str = Body(..., embed=True),
    concentracion: float = Body(..., embed=True),
    unidad: str = Body(..., embed=True)
):
    """Endpoint para agregar un compuesto a un medicamento"""
    result = await MedicamentoService.add_compuesto_to_medicamento(
        medicamento_id, compuesto_id, concentracion, unidad
    )
    # Convert to a dictionary with clear field names for better response
    if result:
        return {
            "success": True,
            "message": "Compuesto added to medicamento successfully",
            "compuesto_id": compuesto_id,
            "medicamento_id": medicamento_id,
            "concentracion": concentracion,
            "unidad_medida": unidad
        }
    return {"success": False, "message": "Failed to add compuesto to medicamento"}

@router.put("/{medicamento_id}", response_model=Medicamento, status_code=status.HTTP_200_OK)
async def update_medicamento(medicamento_id: str, medicamento: Medicamento):
    """Endpoint para actualizar un medicamento"""
    return await MedicamentoService.update_medicamento(medicamento_id, medicamento)

@router.delete("/{medicamento_id}", status_code=status.HTTP_200_OK)
async def delete_medicamento(medicamento_id: str):
    """Endpoint para eliminar un medicamento"""
    result = await MedicamentoService.delete_medicamento(medicamento_id)
    return result