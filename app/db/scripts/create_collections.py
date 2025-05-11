import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

""""
This script creates collections in a MongoDB database with validation rules defined in JSON schema files.
It uses the pymongo library to connect to the database and create collections.
"""

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "medicamentos_db"

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMA_DIR = os.path.join(BASE_DIR, "schemas")

def create_collection(name, schema_filename):
    schema_path = os.path.join(SCHEMA_DIR, schema_filename)
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    try:
        db.create_collection(name, validator=schema["validator"])
        print(f"Collection '{name}' created with validation.")
    except Exception as e:
        print(f"Collection '{name}' already exists or failed: {e}")

# Create all collections
create_collection("compuestos", "compuestos_schema.json")
create_collection("medicamentos", "medicamentos_schema.json")
create_collection("compuestos_por_medicamento", "compuestos_medicamentos_schema.json")
