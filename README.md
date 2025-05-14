# API REST de Medicamentos y Compuestos

Proyecto para la asignatura de Tópicos Avanzados de Base de Datos (TADB) - Examen No. 4

## Descripción

Este proyecto implementa una API REST para gestionar medicamentos y sus compuestos, utilizando un modelo de datos NoSQL basado en MongoDB. La API permite realizar operaciones CRUD sobre medicamentos y compuestos, así como consultar los medicamentos que contienen un determinado compuesto y viceversa.

## Tecnologías utilizadas

- Python 3.10+
- FastAPI
- MongoDB Atlas
- Patrón Repositorio
- Postman (para pruebas)
- GitHub

## Estructura del Proyecto

```
tadb_202510_ex04/
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── compuesto.py
│   │   ├── medicamento.py
│   │   └── compuesto_medicamento.py
│   ├── repositories/
│   │   ├── compuesto_repository.py
│   │   ├── medicamento_repository.py
│   │   └── compuesto_medicamento_repository.py
│   ├── services/
│   │   ├── compuesto_service.py
│   │   ├── medicamento_service.py
│   ├── controllers/
│   │   ├── compuesto_controller.py
│   │   └── medicamento_controller.py
│   ├── db/
│   │   ├── mongo.py
│   │   └── scripts/
│   │       ├── create_collections.py
|   |       ├── import_data.py
│   ├── schemas/
│   │   ├── compuesto_medicamentos_schema.py
│   │   ├── compuestos_schema.json
│   │   └── medicamentos_schema.json
|   ├── datos/
│   |   ├── compuestos.json
│   |   ├── medicamentos.json
│   |   └── compuestos_medicamentos.json
|   ├── docs/
|   |   └── postman/
│   |       └── Medicamentos_API_postman_collection.json
├── ping_db.py
├── README.md
├── requirements.txt
└── .env
```

## Instalación y Configuración

### Requisitos Previos

- Python 3.10+
- MongoDB Atlas cuenta (gratis)
- Git

### Pasos para instalar y ejecutar el proyecto

1. Clonar el repositorio:
```bash
git clone https://github.com/rosvend/tadb_202510_ex04.git
cd tadb_202510_ex04
```

2. Crear un entorno virtual e instalar las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar variables de entorno:
   - Copiar el archivo `.env.example` a `.env`
   - Actualizar las variables con tu configuración de MongoDB Atlas

4. Iniciar la aplicación:
```bash
python -m app.main
```

5. La API estará disponible en: http://localhost:8000
   - La documentación Swagger estará disponible en: http://localhost:8000/docs
   - La documentación ReDoc estará disponible en: http://localhost:8000/redoc

## Modelo de Datos

### Colecciones en MongoDB

1. **compuestos**
   - _id: ObjectId
   - nombre: string

2. **medicamentos**
   - _id: ObjectId
   - nombre: string
   - fabricante: string

3. **compuestos_medicamentos**
   - _id: ObjectId
   - compuesto_id: ObjectId (referencia a compuestos)
   - medicamento_id: ObjectId (referencia a medicamentos)
   - concentracion: number
   - unidad_medida: string

## Endpoints de la API

### Compuestos

- `GET /api/compuestos` - Listar todos los compuestos
- `GET /api/compuestos/{compuesto_id}` - Obtener un compuesto por ID
- `GET /api/compuestos/{compuesto_id}/medicamentos` - Listar medicamentos que contienen un compuesto
- `POST /api/compuestos` - Crear un nuevo compuesto
- `PUT /api/compuestos/{compuesto_id}` - Actualizar un compuesto
- `DELETE /api/compuestos/{compuesto_id}` - Eliminar un compuesto

### Medicamentos

- `GET /api/medicamentos` - Listar todos los medicamentos
- `GET /api/medicamentos/{medicamento_id}` - Obtener un medicamento por ID
- `GET /api/medicamentos/{medicamento_id}/compuestos` - Listar compuestos de un medicamento
- `POST /api/medicamentos` - Crear un nuevo medicamento
- `PUT /api/medicamentos/{medicamento_id}` - Actualizar un medicamento
- `DELETE /api/medicamentos/{medicamento_id}` - Eliminar un medicamento

## Colección de Postman

Para facilitar las pruebas, se incluye una colección de Postman con ejemplos de todas las peticiones en la carpeta `docs/postman`.
