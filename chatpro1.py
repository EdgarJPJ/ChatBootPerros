from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import networkx as nx
import re

app = FastAPI()

# Servir archivos estáticos (JS, CSS)
app.mount("/statics", StaticFiles(directory="statics"), name="statics")

# Configurar plantillas HTML
templates = Jinja2Templates(directory="template")

# Modelo para la pregunta del usuario
class Question(BaseModel):
    pregunta: str

# Crear el grafo de conocimiento con información detallada
G = nx.DiGraph()

# Diccionario para almacenar información detallada sobre cada nodo
info_detallada = {
    # Información general
    "Perros": "Los perros son animales de compañía que requieren cuidados específicos en salud, alimentación, higiene, ejercicio, y entrenamiento para mantenerse felices y saludables.",
    
    # Salud
    "Salud": "La salud de tu perro es fundamental. Incluye visitas regulares al veterinario, vacunación al día, control de parásitos, y estar atento a cambios en su comportamiento o aspecto físico.",
    "Síntomas de emergencia": "Algunos síntomas requieren atención veterinaria inmediata para evitar complicaciones graves o fatales.",
    "Vómitos persistentes": "Si tu perro vomita más de dos veces en 24 horas, podría indicar intoxicación, obstrucción intestinal o enfermedad grave. Requiere atención veterinaria urgente, especialmente si hay sangre o letargo.",
    "Dificultad respiratoria": "Jadeos excesivos, respiración por la boca, o encías azuladas son señales de emergencia. Pueden indicar golpe de calor, problemas cardíacos o alergias severas.",
    "Convulsiones": "Los episodios convulsivos se manifiestan como temblores involuntarios, rigidez, pérdida de conciencia o salivación excesiva. Requieren evaluación médica inmediata.",
    
    "Vacunas": "Las vacunas son esenciales para prevenir enfermedades potencialmente mortales. Se administran según un calendario específico recomendado por tu veterinario.",
    "Calendario de vacunación": "Cachorros: vacunas múltiples entre las 6-16 semanas. Adultos: refuerzos anuales o cada 3 años según la vacuna. Consulta a tu veterinario para un plan personalizado.",
    "Rabia": "Vacuna obligatoria por ley en muchos lugares. Protege contra una enfermedad mortal que puede transmitirse a humanos. Se administra anualmente o cada 3 años según la formulación.",
    "Parvovirus": "Enfermedad altamente contagiosa y potencialmente mortal. La vacuna se incluye en el esquema básico para cachorros y requiere refuerzos periódicos.",
    "Moquillo": "Enfermedad viral grave que afecta múltiples sistemas del cuerpo. La vacuna se administra a cachorros y requiere refuerzos regulares.",
    "Hepatitis": "Infección viral que afecta el hígado, ojos y riñones. La vacuna se incluye en el esquema básico para cachorros.",
    
    "Enfermedades comunes": "Hay varias enfermedades que afectan comúnmente a los perros. Conocerlas te ayudará a identificar síntomas tempranos.",
    "Leptospirosis": "Infección bacteriana transmitida por agua o suelo contaminado con orina de animales infectados. Síntomas: fiebre, dolor muscular, deshidratación, problemas renales o hepáticos. Es zoonótica (puede transmitirse a humanos).",
    "Parvovirosis": "Enfermedad viral extremadamente contagiosa que afecta principalmente a cachorros. Causa diarrea severa con sangre, vómitos, deshidratación y puede ser mortal sin tratamiento rápido.",
    "Tos de las perreras": "Infección respiratoria altamente contagiosa. Síntomas: tos seca persistente, estornudos y secreción nasal. Generalmente se contrae en lugares con muchos perros.",
    "Obesidad": "Condición médica donde el exceso de peso afecta la salud. Causa problemas articulares, cardíacos, diabetes y reduce la esperanza de vida. Se previene con dieta controlada y ejercicio regular.",
    "Alergias": "Reacciones comunes a alimentos, polen, ácaros o picaduras. Síntomas: rascado excesivo, lamido de patas, inflamación de piel, problemas gastrointestinales o respiratorios.",
    
    "Esterilización": "Procedimiento quirúrgico que previene la reproducción. Ofrece beneficios para la salud y el comportamiento de tu mascota.",
    "Beneficios": "Reduce riesgo de cáncer reproductivo, infecciones uterinas, comportamientos indeseados como marcaje territorial, agresividad y escape. Contribuye al control poblacional de animales sin hogar.",
    "Edad recomendada": "Generalmente entre 6-9 meses, aunque puede variar según raza y tamaño. Perros pequeños: 6 meses. Perros grandes: 9-12 meses para permitir desarrollo óseo adecuado. Consulta con tu veterinario.",
    "Cuidados postoperatorios": "Mantener al perro tranquilo por 7-10 días, usar collar isabelino para evitar lamido de puntos, vigilar la herida por signos de infección, y administrar medicamentos según prescripción veterinaria.",
    
    # Alimentación
    "Alimentación": "Una nutrición adecuada es fundamental para la salud y longevidad de tu perro. Debe adaptarse a su edad, tamaño, nivel de actividad y necesidades específicas.",
    "Tipos de comida": "Existen diversas opciones: alimento seco (croquetas), húmedo (enlatado), dieta BARF (alimentos crudos), comida casera o dietas prescritas por veterinarios. Cada tipo tiene ventajas y consideraciones específicas según las necesidades de tu perro.",
    "Frecuencia": "Cachorros (2-6 meses): 3-4 veces al día. Perros jóvenes (6-12 meses): 2-3 veces al día. Adultos: 1-2 veces al día. Razas propensas a torsión gástrica deben recibir porciones pequeñas más frecuentes.",
    "Alimentos prohibidos": "Ciertos alimentos humanos son tóxicos o perjudiciales para los perros y deben evitarse completamente.",
    "Chocolate": "Contiene teobromina y cafeína, tóxicas para perros. Puede causar vómitos, diarrea, ritmo cardíaco irregular, convulsiones e incluso la muerte. El chocolate oscuro es más peligroso que el con leche.",
    "Uvas/pasas": "Pueden causar fallo renal agudo incluso en pequeñas cantidades. Los síntomas incluyen vómitos, diarrea, letargo y disminución de la producción de orina.",
    "Cebolla/ajo": "Contienen compuestos que dañan los glóbulos rojos, causando anemia. Peligrosos en cualquier forma: crudos, cocidos, en polvo o deshidratados.",
    "Xilitol": "Edulcorante artificial presente en chicles, caramelos y productos horneados. Causa liberación masiva de insulina, hipoglucemia, fallo hepático y puede ser mortal rápidamente.",
    "Suplementos": "Algunos perros pueden necesitar suplementos específicos como ácidos grasos omega-3 para pelaje y articulaciones, probióticos para salud digestiva, o condroprotectores para perros mayores o con problemas articulares. Siempre consúltalo con tu veterinario.",
    
    # Higiene
    "Higiene": "Mantener una buena higiene es esencial para la salud de tu perro y para una convivencia agradable en el hogar.",
    "Baño": "Frecuencia: cada 4-6 semanas para la mayoría de razas, ajustando según actividad y tipo de pelaje. Usar champú específico para perros (pH diferente al humano). El baño excesivo puede causar sequedad y problemas de piel.",
    "Cepillado": "Perros de pelo corto: cepillado semanal con cepillo de cerdas. Pelo medio: 2-3 veces por semana con cepillo de púas. Pelo largo: cepillado diario para evitar nudos. Pelaje doble: cepillado frecuente en épocas de muda con rastrillo especial.",
    "Corte de uñas": "Realizar cada 3-4 semanas. Cortar solo la punta para evitar cortar el 'quick' (vaso sanguíneo). Si las uñas son oscuras, cortar pequeñas porciones. El sonido de uñas en el suelo indica que necesitan corte.",
    "Limpieza dental": "Cepillado dental idealmente diario con pasta específica para perros. Complementar con juguetes dentales, snacks específicos o aditivos para agua. La acumulación de sarro puede causar enfermedad periodontal, mal aliento y problemas cardíacos.",
    
    # Ejercicio
    "Ejercicio": "El ejercicio regular es crucial para la salud física y mental de tu perro. Previene obesidad, problemas de comportamiento y fortalece el vínculo con el dueño.",
    "Frecuencia según raza": "Razas activas (Border Collie, Husky): 1-2 horas diarias de actividad intensa. Razas medianas (Labrador, Boxer): 30-60 minutos diarios. Razas pequeñas o braquicéfalas (Bulldog, Pug): 15-30 minutos de actividad moderada. Perros mayores o con problemas de salud: actividad suave pero regular.",
    "Actividades recomendadas": "Paseos diarios, juegos de buscar, natación (excelente para articulaciones), agilidad, juegos de inteligencia, socialización con otros perros. Variar las actividades previene el aburrimiento y estimula mental y físicamente.",
    "Beneficios": "Control de peso, salud cardiovascular, reducción del estrés y ansiedad, mejora del sueño, prevención de problemas de comportamiento destructivo, fortalecimiento de articulaciones y músculos, y estimulación mental.",
    
    # Comportamiento
    "Comportamiento": "Entender el comportamiento canino te ayudará a tener una mejor relación con tu perro y prevenir problemas.",
    "Agresividad": "Puede manifestarse por miedo, territorialidad, protección de recursos o dolor. Señales de advertencia: gruñidos, mostrar dientes, postura rígida. Requiere evaluación profesional para determinar causas y tratamiento. Nunca castigar la agresividad pues puede empeorarla.",
    "Socialización": "Proceso crucial entre 3-14 semanas de vida. Exponer positivamente al cachorro a diferentes personas, animales, entornos, sonidos y experiencias. Continuar en la adultez con encuentros positivos. Previene miedos y comportamientos problemáticos futuros.",
    "Ansiedad por separación": "Malestar severo cuando el perro queda solo. Síntomas: destrucción, ladridos excesivos, intentos de escape, eliminar en casa. Tratamiento: desensibilización gradual, rutinas de partida/llegada sin drama, ejercicio antes de salir, juguetes de enriquecimiento.",
    
    # Entrenamiento
    "Entrenamiento": "El entrenamiento positivo fortalece la relación con tu perro y asegura una convivencia armoniosa. Debe basarse en refuerzos positivos, no en castigos.",
    "Órdenes básicas": "Sentado, quieto, ven, junto y dejar son comandos esenciales para la seguridad y control. Enseñar con sesiones cortas (5-10 minutos) varias veces al día, usando refuerzos positivos inmediatos (premios, caricias o juego).",
    "Refuerzo positivo": "Técnica que premia comportamientos deseados en lugar de castigar los indeseados. Usar premios de alto valor (comida especial, juguetes favoritos), timing preciso y marcadores como clicker. Más efectivo y crea un perro más confiado que el castigo.",
    "Obediencia avanzada": "Incluye comandos como permanecer quieto con distracciones, caminar sin tirar con diferentes estímulos, acudir al llamado desde distancia, y comportamientos específicos como saludar sin saltar. Requiere constancia y práctica gradual en diferentes entornos.",
    
    # Cuidados generales
    "Cuidados generales": "Aspectos importantes para proporcionar una vida equilibrada y segura a tu perro.",
    "Espacio ideal": "Todos los perros necesitan un lugar tranquilo, cómodo y seguro para descansar. Debe ser accesible pero permitirles retirarse cuando necesiten tranquilidad. Áreas separadas para comer, dormir y hacer sus necesidades. Incluso en espacios pequeños, organizar zonas definidas.",
    "Juguetes recomendados": "Rotativos para mantener interés. Incluir: juguetes de masticación (huesos de nylon) para higiene dental, interactivos para estimulación mental (dispensadores de comida), peluches si no los destruye, y juguetes para ejercicio (pelotas, discos). Supervisar uso para evitar ingesta de piezas.",
    "Convivencia con niños/mascotas": "Supervisión constante con niños pequeños. Enseñar a ambos a respetar espacio y señales. Introducción gradual con otras mascotas: primero por olor, luego visión controlada y finalmente interacción supervisada. Cada animal debe tener su espacio, recursos y atención.",
    
    # Razas
    "Razas": "Existen más de 300 razas de perros reconocidas, cada una con características físicas y de comportamiento específicas. Conocer las particularidades de tu raza te ayudará a satisfacer mejor sus necesidades.",
    "Labrador": "Raza popular de tamaño mediano-grande, amigable, sociable y excelente con familias. Requiere ejercicio diario y tiene tendencia a la obesidad si no se controla su alimentación.",
    "Necesidad de ejercicio: Alta": "Requieren mínimo 1 hora diaria de actividad física vigorosa. Disfrutan natación, juegos de recuperación y caminatas largas. Sin suficiente ejercicio desarrollan problemas de comportamiento como masticar objetos o hiperactividad.",
    "Propensión a obesidad": "Alta tendencia genética a ganar peso. Controlar porciones estrictamente, evitar alimentar entre comidas, usar premios bajos en calorías para entrenamiento y monitorear peso regularmente. La obesidad puede causar problemas articulares, diabetes y reducir su esperanza de vida.",
    
    "Pastor Alemán": "Raza inteligente, leal y versátil de tamaño grande. Requiere estimulación mental y física considerable. Excelente para entrenamiento, trabajo y compañía.",
    "Cuidado de cadera": "Propensos a displasia de cadera. Mantener peso óptimo, ejercicio adecuado sin saltos excesivos en cachorros, suplementación con condroprotectores según recomendación veterinaria y considerar radiografías preventivas para detección temprana.",
    "Entrenamiento recomendado": "Se benefician de entrenamiento estructurado desde cachorros. Excelentes en obediencia, rastreo, agilidad y deportes caninos. Necesitan desafíos mentales regulares para evitar aburrimiento y comportamientos destructivos. Responden mejor a métodos positivos consistentes.",
    
    "Chihuahua": "Raza más pequeña del mundo, con gran personalidad. Longevos, leales y alertas. Requieren cuidados específicos por su tamaño reducido.",
    "Protección contra el frío": "Extremadamente sensibles a temperaturas bajas. En invierno necesitan ropa adecuada para exteriores, limitar tiempo en ambientes fríos, usar camas térmicas o mantas, y mantener la casa a temperatura adecuada. La hipotermia puede ocurrir rápidamente.",
    "Socialización temprana": "Particularmente importante para evitar agresividad por miedo. Exposición gradual y positiva a personas de diferentes edades, otros animales y situaciones diversas. Tendencia a ser reservados con extraños si no se socializan adecuadamente.",
    
    "Husky": "Raza nórdica energética, independiente y de espíritu libre. Originalmente criados para tirar de trineos en largas distancias.",
    "Ejercicio intenso diario": "Necesitan mínimo 2 horas de ejercicio vigoroso diario. Idealas: correr junto a bicicleta, canicross, largas caminatas o natación. Sin suficiente ejercicio, desarrollan comportamientos destructivos severos y pueden escaparse buscando actividad.",
    "Cuidado del pelaje": "Pelaje doble que requiere cepillado 2-3 veces por semana y diario en épocas de muda (primavera/otoño). No rasurar en verano pues el subpelo protege de calor y rayos UV. Baños ocasionales para no eliminar aceites naturales."
}


for origen, destino in [
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
]:
    G.add_edge(origen, destino)
    
    # Asegurar que ambos nodos tengan información detallada
    if origen not in info_detallada:
        info_detallada[origen] = f"Información sobre {origen}"
    if destino not in info_detallada:
        info_detallada[destino] = f"Información sobre {destino}"

# Función mejorada para buscar información relevante
def buscar_informacion(texto):
    texto = texto.lower()
    resultados = []
    
    # Lista de palabras clave a ignorar en la búsqueda
    palabras_ignorar = ["mi", "el", "la", "los", "las", "un", "una", "unos", "unas", "por", "para", "como", "qué", "cuando", "donde"]
    
    # Extraer palabras clave de la pregunta
    palabras = re.findall(r'\b\w+\b', texto)
    palabras_clave = [p for p in palabras if len(p) > 3 and p not in palabras_ignorar]
    
    # Buscar coincidencias directas en nodos
    for nodo in G.nodes():
        nodo_lower = nodo.lower()
        # Verificar coincidencia exacta
        if nodo_lower in texto:
            info = info_detallada.get(nodo, f"Información sobre {nodo}")
            subtemas = list(G.successors(nodo))
            if subtemas:
                subtemas_str = ", ".join(subtemas)
                resultados.append({
                    "tema": nodo,
                    "descripcion": info,
                    "subtemas": subtemas
                })
            else:
                resultados.append({
                    "tema": nodo,
                    "descripcion": info,
                    "subtemas": []
                })
        # Verificar coincidencia parcial con palabras clave
        elif any(p in nodo_lower for p in palabras_clave):
            info = info_detallada.get(nodo, f"Información sobre {nodo}")
            subtemas = list(G.successors(nodo))
            resultados.append({
                "tema": nodo,
                "descripcion": info,
                "subtemas": subtemas
            })
    
    # Si no hay resultados, buscar en temas generales
    if not resultados:
        temas_generales = ["Salud", "Alimentación", "Higiene", "Ejercicio", "Comportamiento", "Entrenamiento", "Cuidados generales", "Razas"]
        for tema in temas_generales:
            if any(p in tema.lower() for p in palabras_clave) or any(p in info_detallada.get(tema, "").lower() for p in palabras_clave):
                resultados.append({
                    "tema": tema,
                    "descripcion": info_detallada.get(tema, f"Información sobre {tema}"),
                    "subtemas": list(G.successors(tema))
                })
    
    return resultados

# Función para responder preguntas de manera más completa
def responder_pregunta(pregunta):
    resultados = buscar_informacion(pregunta)
    
    if not resultados:
        return {
            "respuesta": "No encontré información específica sobre tu pregunta. Puedes consultar sobre salud, alimentación, higiene, ejercicio, comportamiento, entrenamiento, cuidados generales o razas específicas de perros.",
            "temas_relacionados": ["Salud", "Alimentación", "Higiene", "Ejercicio", "Comportamiento", "Entrenamiento", "Cuidados generales", "Razas"]
        }
    
    # Construir respuesta con la información más relevante
    respuesta = ""
    temas_relacionados = []
    
    # Limitar a los 3 resultados más relevantes para no sobrecargar
    for resultado in resultados[:3]:
        respuesta += f"📌 {resultado['tema']}: {resultado['descripcion']}\n\n"
        temas_relacionados.extend(resultado['subtemas'])
    
    # Eliminar duplicados en temas relacionados
    temas_relacionados = list(set(temas_relacionados))
    
    return {
        "respuesta": respuesta.strip(),
        "temas_relacionados": temas_relacionados[:5]  # Limitamos a 5 temas relacionados
    }

# Ruta API para recibir preguntas
@app.post("/preguntar/")
async def preguntar(question: Question):
    return responder_pregunta(question.pregunta)

# Ruta para la página principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta para obtener información específica de un tema
@app.get("/tema/{nombre_tema}")
async def get_tema(nombre_tema: str):
    if nombre_tema in info_detallada:
        subtemas = list(G.successors(nombre_tema))
        return {
            "tema": nombre_tema,
            "descripcion": info_detallada[nombre_tema],
            "subtemas": [{"nombre": s, "descripcion": info_detallada.get(s, "")} for s in subtemas]
        }
    return JSONResponse(
        status_code=404,
        content={"mensaje": "Tema no encontrado"}
    )