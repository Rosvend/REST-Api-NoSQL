import json
import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

"""
This script imports data from JSON files in the datos/ directory into MongoDB collections.
It uses the pymongo library to connect to the database and insert data.
"""

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "medicamentos_db"

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Paths to JSON files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, "datos")

def import_data(collection_name, filename):
    """Import data from a JSON file into a MongoDB collection"""
    file_path = os.path.join(DATA_DIR, filename)
    
    db[collection_name].delete_many({})
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for item in data:
        if "_id" in item and "$oid" in item["_id"]:
            item["_id"] = ObjectId(item["_id"]["$oid"])
        
        if "medicamento_id" in item and "$oid" in item["medicamento_id"]:
            item["medicamento_id"] = ObjectId(item["medicamento_id"]["$oid"])
            
        if "compuesto_id" in item and "$oid" in item["compuesto_id"]:
            item["compuesto_id"] = ObjectId(item["compuesto_id"]["$oid"])
    
    # Insertar datos
    if data:
        result = db[collection_name].insert_many(data)
        print(f"Imported {len(result.inserted_ids)} documents into {collection_name}")
    else:
        print(f"No data to import into {collection_name}")

def main():
    try:
        print("Creating collections with schemas...")
        from app.db.scripts.create_collections import create_collection
        
        # Importar datos
        print("\nImporting data into collections...")
        import_data("compuestos", "compuestos.json")
        import_data("medicamentos", "medicamentos.json")
        import_data("compuestos_por_medicamento", "compuestos_medicamentos.json")
        
        print("\nData import completed successfully!")
    except Exception as e:
        print(f"Error during import: {e}")

if __name__ == "__main__":
    main()