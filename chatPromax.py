from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

# Servir archivos estáticos (JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar plantillas HTML
templates = Jinja2Templates(directory="template")

# Modelo para la pregunta del usuario
class Question(BaseModel):
    pregunta: str

# Crear el grafo de conocimiento
G = nx.DiGraph()
nodos = [
    # Categoría principal
    ("Perros", "Salud"), 
    ("Perros", "Alimentación"),
    ("Perros", "Higiene"), 
    ("Perros", "Ejercicio"),
    ("Perros", "Comportamiento"), 
    ("Perros", "Entrenamiento"),
    ("Perros", "Cuidados generales"),
    ("Perros", "Razas"),

    # Salud
    ("Salud", "Síntomas de emergencia"),
    ("Salud", "Vacunas"), 
    ("Salud", "Enfermedades comunes"),
    ("Salud", "Esterilización"),
    
    # Síntomas de emergencia (subnodos)
    ("Síntomas de emergencia", "Vómitos persistentes"),
    ("Síntomas de emergencia", "Dificultad respiratoria"),
    ("Síntomas de emergencia", "Convulsiones"),
    
    # Vacunas
    ("Vacunas", "Calendario de vacunación"),
    ("Vacunas", "Rabia"),
    ("Vacunas", "Parvovirus"),
    ("Vacunas", "Moquillo"),
    ("Vacunas", "Hepatitis"),
    
    # Enfermedades comunes
    ("Enfermedades comunes", "Moquillo"),
    ("Enfermedades comunes", "Leptospirosis"),
    ("Enfermedades comunes", "Parvovirosis"),
    ("Enfermedades comunes", "Tos de las perreras"),
    ("Enfermedades comunes", "Obesidad"),
    ("Enfermedades comunes", "Alergias"),
    
    # Detalles enfermedades
    ("Moquillo", "Enfermedad viral contagiosa que afecta sistemas respiratorio y nervioso"),
    ("Leptospirosis", "Infección bacteriana transmitida por agua contaminada"),
    ("Parvovirosis", "Enfermedad gastrointestinal grave con alta mortalidad en cachorros"),
    
    # Esterilización
    ("Esterilización", "Beneficios"),
    ("Esterilización", "Edad recomendada"),
    ("Esterilización", "Cuidados postoperatorios"),
    
    # Alimentación
    ("Alimentación", "Tipos de comida"),
    ("Alimentación", "Frecuencia"),
    ("Alimentación", "Alimentos prohibidos"),
    ("Alimentación", "Suplementos"),
    
    ("Alimentos prohibidos", "Chocolate"),
    ("Alimentos prohibidos", "Uvas/pasas"),
    ("Alimentos prohibidos", "Cebolla/ajo"),
    ("Alimentos prohibidos", "Xilitol"),
    
    # Higiene
    ("Higiene", "Baño"),
    ("Higiene", "Cepillado"),
    ("Higiene", "Corte de uñas"),
    ("Higiene", "Limpieza dental"),
    
    # Ejercicio
    ("Ejercicio", "Frecuencia según raza"),
    ("Ejercicio", "Actividades recomendadas"),
    ("Ejercicio", "Beneficios"),
    
    # Comportamiento
    ("Comportamiento", "Agresividad"),
    ("Comportamiento", "Socialización"),
    ("Comportamiento", "Ansiedad por separación"),
    
    # Entrenamiento
    ("Entrenamiento", "Órdenes básicas"),
    ("Entrenamiento", "Refuerzo positivo"),
    ("Entrenamiento", "Obediencia avanzada"),
    
    # Cuidados generales
    ("Cuidados generales", "Espacio ideal"),
    ("Cuidados generales", "Juguetes recomendados"),
    ("Cuidados generales", "Convivencia con niños/mascotas"),
    
    # Razas
    ("Razas", "Labrador"),
    ("Razas", "Pastor Alemán"),
    ("Razas", "Chihuahua"),
    ("Razas", "Husky"),
    
    # Especificaciones por raza
    ("Labrador", "Necesidad de ejercicio: Alta"),
    ("Labrador", "Propensión a obesidad"),
    ("Pastor Alemán", "Cuidado de cadera"),
    ("Pastor Alemán", "Entrenamiento recomendado"),
    ("Chihuahua", "Protección contra el frío"),
    ("Chihuahua", "Socialización temprana"),
    ("Husky", "Ejercicio intenso diario"),
    ("Husky", "Cuidado del pelaje")
]
G.add_edges_from(nodos)

# Función para responder preguntas
def responder_pregunta(pregunta):
    pregunta = pregunta.lower()
    for nodo in G.nodes:
        if nodo.lower() in pregunta:
            subtemas = list(G.successors(nodo))
            return {"respuesta": f"Información sobre {nodo}: {', '.join(subtemas)}"}
    return {"respuesta": "No encontré información exacta."}

# Ruta API para recibir preguntas
@app.post("/preguntar/")
async def preguntar(question: Question):
    return responder_pregunta(question.pregunta)

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})