from bson import ObjectId
from typing import List, Optional
from app.db.mongo import db
from app.models.compuesto_med import CompuestoPorMedicamento

class CompuestoPorMedicamentoRepository:
    """Repository for CompuestoPorMedicamento entity operations"""
    
    collection = db.compuestos_por_medicamento
    
    @staticmethod
    async def get_all() -> List[CompuestoPorMedicamento]:
        """Get all compuestos por medicamento from the database"""
        compuestos_med = []
        cursor = CompuestoPorMedicamentoRepository.collection.find({})
        async for document in cursor:
            document["_id"] = str(document["_id"])
            document["medicamento_id"] = str(document["medicamento_id"])
            document["compuesto_id"] = str(document["compuesto_id"])
            compuestos_med.append(CompuestoPorMedicamento(**document))
        return compuestos_med
    
    @staticmethod
    async def get_by_id(id: str) -> Optional[CompuestoPorMedicamento]:
        """Get a compuesto por medicamento by its ID"""
        try:
            document = await CompuestoPorMedicamentoRepository.collection.find_one({"_id": ObjectId(id)})
            if document:
                document["_id"] = str(document["_id"])
                document["medicamento_id"] = str(document["medicamento_id"])
                document["compuesto_id"] = str(document["compuesto_id"])
                return CompuestoPorMedicamento(**document)
            return None
        except Exception:
            return None
    
    @staticmethod
    async def create(compuesto_med: dict) -> CompuestoPorMedicamento:
        """Create a new compuesto por medicamento"""
        # Convert string IDs to ObjectIds
        if "medicamento_id" in compuesto_med and isinstance(compuesto_med["medicamento_id"], str):
            compuesto_med["medicamento_id"] = ObjectId(compuesto_med["medicamento_id"])
        
        if "compuesto_id" in compuesto_med and isinstance(compuesto_med["compuesto_id"], str):
            compuesto_med["compuesto_id"] = ObjectId(compuesto_med["compuesto_id"])
        
        # Ensure _id is not included
        if "_id" in compuesto_med:
            del compuesto_med["_id"]
        
        result = await CompuestoPorMedicamentoRepository.collection.insert_one(compuesto_med)
        
        # Return the created relation with the generated ID
        return await CompuestoPorMedicamentoRepository.get_by_id(str(result.inserted_id))
    
    @staticmethod
    async def delete_by_medicamento_id(medicamento_id: str) -> int:
        """Delete all compuestos por medicamento for a specific medicamento"""
        result = await CompuestoPorMedicamentoRepository.collection.delete_many(
            {"medicamento_id": ObjectId(medicamento_id)}
        )
        return result.deleted_count
    
    @staticmethod
    async def delete_by_compuesto_id(compuesto_id: str) -> int:
        """Delete all compuestos por medicamento for a specific compuesto"""
        result = await CompuestoPorMedicamentoRepository.collection.delete_many(
            {"compuesto_id": ObjectId(compuesto_id)}
        )
        return result.deleted_count