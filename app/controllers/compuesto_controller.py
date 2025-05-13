from fastapi import APIRouter, status, Response
from typing import List, Dict, Any
from app.models.compuesto import Compuesto
from app.services.compuesto_service import CompuestoService


router = APIRouter(prefix="/api/compuestos", tags=["compuestos"])

@router.get("/",response_model=List[Compuesto],status_code=status.HTTP_200_OK)
async def get_all_compuestos() -> List[Compuesto]:
    """Endpoint para obtener todos los compuestos"""
    return await CompuestoService.get_all_compuestos()

@router.get("/{compuesto_id}", response_model=Compuesto, status_code=status.HTTP_200_OK)
async def get_compuesto_by_id(compuesto_id: str) -> Compuesto:
    """Endpoint para obtener un compuesto por su ID"""
    return await CompuestoService.get_compuesto_by_id(compuesto_id)

@router.get("/{compuesto_id}/medicamentos",status_code=status.HTTP_200_OK)
async def get_medicamentos_by_compuesto(compuesto_id: str):
    """Endpoint para obtener medicamentos por ID de compuesto"""
    return await CompuestoService.get_medicamentos_by_compuesto(compuesto_id)

@router.post("/", response_model=Compuesto, status_code=status.HTTP_201_CREATED)
async def create_compuesto(compuesto: Compuesto):
    """Endpoint para crear un nuevo compuesto"""
    return await CompuestoService.create_compuesto(compuesto)

@router.put("/{compuesto_id}", response_model=Compuesto, status_code=status.HTTP_200_OK)
async def update_compuesto(compuesto_id: str, compuesto: Compuesto):
    """Endpoint para actualizar un compuesto"""
    return await CompuestoService.update_compuesto(compuesto_id, compuesto)

@router.delete("/{compuesto_id}", status_code=status.HTTP_200_OK)
async def delete_compuesto(compuesto_id: str):
    """Endpoint para eliminar un compuesto"""
    result = await CompuestoService.delete_compuesto(compuesto_id)
    return result