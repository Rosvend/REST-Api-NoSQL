from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.compuesto_controller import router as compuesto_router
from app.controllers.medicamento_controller import router as medicamento_router

app = FastAPI(
    title="API de Medicamentos y Compuestos",
    description="API REST para gestionar medicamentos y sus compuestos químicos",
    version="1.0.0",
)

# Configuracion de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compuesto_router)
app.include_router(medicamento_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "API de Medicamentos y Compuestos",
        "documentation": "/docs",
        "endpoints": [
            "/api/compuestos",
            "/api/medicamentos"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)