from bson import ObjectId
from typing import List, Optional
from app.db.mongo import db
from app.models.compuesto import Compuesto

class CompuestoRepository:
    """Repository for Compuesto entity operations"""
    
    collection = db.compuestos
    
    @staticmethod
    async def get_all() -> List[Compuesto]:
        """Get all compuestos from the database"""
        compuestos = []
        cursor = CompuestoRepository.collection.find({})
        async for document in cursor:
            document["_id"] = str(document["_id"])
            compuestos.append(Compuesto(**document))
        return compuestos
    
    @staticmethod
    async def get_by_id(id: str) -> Optional[Compuesto]:
        """Get a compuesto by its ID"""
        try:
            document = await CompuestoRepository.collection.find_one({"_id": ObjectId(id)})
            if document:
                document["_id"] = str(document["_id"])
                return Compuesto(**document)
            return None
        except Exception:
            return None
    
    @staticmethod
    async def create(compuesto: Compuesto) -> Compuesto:
        """Create a new compuesto"""
        # Ensure ID is not included in the insert operation
        compuesto_dict = compuesto.dict(exclude_unset=True)
        if "_id" in compuesto_dict:
            del compuesto_dict["_id"]
        
        result = await CompuestoRepository.collection.insert_one(compuesto_dict)
        
        # Return the created compuesto with the generated ID
        created_compuesto = await CompuestoRepository.get_by_id(str(result.inserted_id))
        return created_compuesto
    
    @staticmethod
    async def update(id: str, compuesto: Compuesto) -> Optional[Compuesto]:
        """Update an existing compuesto"""
        compuesto_dict = compuesto.dict(exclude_unset=True)
        if "_id" in compuesto_dict:
            del compuesto_dict["_id"]
            
        await CompuestoRepository.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": compuesto_dict}
        )
        
        # Return the updated compuesto
        return await CompuestoRepository.get_by_id(id)
    
    @staticmethod
    async def delete(id: str) -> bool:
        """Delete a compuesto by its ID"""
        result = await CompuestoRepository.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def get_medicamentos_by_compuesto_id(compuesto_id: str) -> List[dict]:
        """Get all medicamentos that contain a specific compuesto"""
        pipeline = [
            {"$match": {"compuesto_id": ObjectId(compuesto_id)}},
            {"$lookup": {
                "from": "medicamentos",
                "localField": "medicamento_id",
                "foreignField": "_id",
                "as": "medicamento"
            }},
            {"$unwind": "$medicamento"},
            {"$project": {
                "_id": {"$toString": "$medicamento._id"},
                "nombre": "$medicamento.nombre",
                "fabricante": "$medicamento.fabricante",
                "concentracion": "$concentracion",
                "unidad_medida": "$unidad_medida"
            }}
        ]
        
        result = []
        cursor = db.compuestos_por_medicamento.aggregate(pipeline)
        async for doc in cursor:
            result.append(doc)
        
        return result