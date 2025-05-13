# Project Requirements Document

## 📘 Project Title
Compuestos de Medicamentos - API REST (NoSQL + Repository Pattern)

## 🎓 Course Info
- 📚 Course: Tópicos Avanzados de Base de Datos  
- 🏫 Universidad Pontificia Bolivariana  
- 👨‍🏫 Docente: Juan D. Rodas (GitHub: `jdrodas`)  
- 🗓 Periodo: 202510  
- 📊 Evaluación: Examen No. 4 – Valor 20%  

## 📅 Deadline
🕕 Entrega: Miércoles 14 de mayo de 2025, 6:00 pm (GMT -5)  
⚠️ No se aceptan entregas fuera de plazo.  

---

## 💡 Objective
Desarrollar una API REST con patrón de diseño Repository sobre una base de datos NoSQL orientada a documentos (preferiblemente MongoDB), para gestionar medicamentos y sus compuestos químicos.

## 🛠️ Stack

- 🧩 Base de Datos: MongoDB Atlas
- 💻 Lenguajes permitidos: Python
- 💻 Framework: FastAPI
- 🧪 Herramientas: Postman, GitHub

---

## 📦 Deliverables

1. **Repositorio GitHub**
   - Nombre: `tadb_202510_ex04`
   - Tipo: Privado
   - Invitar al docente: `jdrodas` como colaborador
   - Evidencia de trabajo colaborativo (commits de todos los miembros)

2. **README.md**
   - Instrucciones para compilar y ejecutar la solución

3. **Datos (carpeta `Datos/`)**
   - Script de creación del modelo de datos (JSON Schema)
   - Archivos `.json` con la información migrada

4. **Notificación**
   - Enviar al correo juand.rodasm@upb.edu.co
     - URL del repositorio
     - Nombres de los estudiantes participantes

---

## 🧬 Data Model

### 1. Colecciones:

- `compuestos`
  - `_id` (ObjectID)
  - `nombre` (string)

- `medicamentos`
  - `_id` (ObjectID)
  - `nombre` (string)
  - `fabricante` (string)

- `compuestos_por_medicamento`
  - `_id_compuesto` (ref ObjectID)
  - `_id_medicamento` (ref ObjectID)
  - `concentracion` (number)
  - `unidad_medida` (string)

### 2. Ejemplo de datos:

| Medicamento | Compuesto                | Concentración | Unidad |
|-------------|--------------------------|---------------|--------|
| Noxpirin    | Acetaminofén             | 500           | mg     |
| Noxpirin    | Cetirizina               | 5             | mg     |
| Noxpirin    | Cafeína                  | 30            | mg     |
| Noxpirin    | Fenilefrina Clorhidrato  | 10            | mg     |

---

## 🧱 API Requirements

Organización en capas: Controller → Service → Repository → Model → Context

Controller: Handling requests and responses associated with HTTP verbs.
Service: Implementing business rule validations.
Repository: Executing CRUD actions associated with each operation.
Model: Classes that define the state and behavior of entities.
Context: Connection to the database.

### 🧪 Endpoints (12 total)

#### Compuestos
- `GET /api/compuestos`
- `GET /api/compuestos/{compuesto_id}`
- `GET /api/compuestos/{compuesto_id}/medicamentos`
- `POST /api/compuestos`
- `PUT /api/compuestos`
- `DELETE /api/compuestos/{compuesto_id}`

#### Medicamentos
- `GET /api/medicamentos`
- `GET /api/medicamentos/{medicamento_id}`
- `GET /api/medicamentos/{medicamento_id}/compuestos`
- `POST /api/medicamentos`
- `PUT /api/medicamentos`
- `DELETE /api/medicamentos/{medicamento_id}`

⚠️ Validar funcionalidad con al menos 3 medicamentos con compuestos compartidos.

---

## ✅ Evaluation Rubric

| Criterio                                          | Valor |
|--------------------------------------------------|-------|
| Repositorio GitHub (estructura, commits, etc.)   | 20%   |
| Modelo de datos + Scripts + Carga JSON           | 20%   |
| Implementación de endpoints (12 x 5%)            | 60%   |


## ⚠️ Important Notes
- No se permite el uso de OneDrive ni Microsoft Teams para compartir entregables.
- No hay supletorios sin autorización oficial.