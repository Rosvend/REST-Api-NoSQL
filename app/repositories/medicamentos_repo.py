from bson import ObjectId
from typing import List, Optional
from app.db.mongo import db
from app.models.medicamento import Medicamento

class MedicamentoRepository:
    """Repository for Medicamento entity operations"""
    
    collection = db.medicamentos
    
    @staticmethod
    async def get_all() -> List[Medicamento]:
        """Get all medicamentos from the database"""
        medicamentos = []
        cursor = MedicamentoRepository.collection.find({})
        async for document in cursor:
            document["_id"] = str(document["_id"])
            medicamentos.append(Medicamento(**document))
        return medicamentos
    
    @staticmethod
    async def get_by_id(id: str) -> Optional[Medicamento]:
        """Get a medicamento by its ID"""
        try:
            document = await MedicamentoRepository.collection.find_one({"_id": ObjectId(id)})
            if document:
                document["_id"] = str(document["_id"])
                return Medicamento(**document)
            return None
        except Exception:
            return None
    
    @staticmethod
    async def create(medicamento: Medicamento) -> Medicamento:
        """Create a new medicamento"""
        # Ensure ID is not included in the insert operation
        medicamento_dict = medicamento.dict(exclude_unset=True)
        if "_id" in medicamento_dict:
            del medicamento_dict["_id"]
        
        result = await MedicamentoRepository.collection.insert_one(medicamento_dict)
        
        # Return the created medicamento with the generated ID
        created_medicamento = await MedicamentoRepository.get_by_id(str(result.inserted_id))
        return created_medicamento
    
    @staticmethod
    async def update(id: str, medicamento: Medicamento) -> Optional[Medicamento]:
        """Update an existing medicamento"""
        medicamento_dict = medicamento.dict(exclude_unset=True)
        if "_id" in medicamento_dict:
            del medicamento_dict["_id"]
            
        await MedicamentoRepository.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": medicamento_dict}
        )
        
        # Return the updated medicamento
        return await MedicamentoRepository.get_by_id(id)
    
    @staticmethod
    async def delete(id: str) -> bool:
        """Delete a medicamento by its ID"""
        result = await MedicamentoRepository.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def get_compuestos_by_medicamento_id(medicamento_id: str) -> List[dict]:
        """Get all compuestos that are in a specific medicamento"""
        pipeline = [
            {"$match": {"medicamento_id": ObjectId(medicamento_id)}},
            {"$lookup": {
                "from": "compuestos",
                "localField": "compuesto_id",
                "foreignField": "_id",
                "as": "compuesto"
            }},
            {"$unwind": "$compuesto"},
            {"$project": {
                "_id": {"$toString": "$compuesto._id"},
                "nombre": "$compuesto.nombre",
                "concentracion": "$concentracion",
                "unidad_medida": "$unidad_medida"
            }}
        ]
        
        result = []
        cursor = db.compuestos_por_medicamento.aggregate(pipeline)
        async for doc in cursor:
            result.append(doc)
        
        return result