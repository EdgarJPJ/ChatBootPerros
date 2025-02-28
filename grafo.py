import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as PathEffects

# Crear el grafo dirigido
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

# Definimos las categorías y sus colores
categorias = {
    "Raíz": ["Perros"],
    "Salud": ["Salud", "Síntomas de emergencia", "Vacunas", "Enfermedades comunes", "Esterilización", 
              "Vómitos persistentes", "Dificultad respiratoria", "Convulsiones",
              "Calendario de vacunación", "Rabia", "Parvovirus", "Moquillo", "Hepatitis",
              "Leptospirosis", "Parvovirosis", "Tos de las perreras", "Obesidad", "Alergias",
              "Beneficios", "Edad recomendada", "Cuidados postoperatorios"],
    "Alimentación": ["Alimentación", "Tipos de comida", "Frecuencia", "Alimentos prohibidos", "Suplementos",
                     "Chocolate", "Uvas/pasas", "Cebolla/ajo", "Xilitol"],
    "Higiene": ["Higiene", "Baño", "Cepillado", "Corte de uñas", "Limpieza dental"],
    "Ejercicio": ["Ejercicio", "Frecuencia según raza", "Actividades recomendadas", "Beneficios"],
    "Comportamiento": ["Comportamiento", "Agresividad", "Socialización", "Ansiedad por separación"],
    "Entrenamiento": ["Entrenamiento", "Órdenes básicas", "Refuerzo positivo", "Obediencia avanzada"],
    "Cuidados generales": ["Cuidados generales", "Espacio ideal", "Juguetes recomendados", "Convivencia con niños/mascotas"],
    "Razas": ["Razas", "Labrador", "Pastor Alemán", "Chihuahua", "Husky", 
              "Necesidad de ejercicio: Alta", "Propensión a obesidad", "Cuidado de cadera", 
              "Entrenamiento recomendado", "Protección contra el frío", "Socialización temprana", 
              "Ejercicio intenso diario", "Cuidado del pelaje"]
}

# Asignamos categoría "Otros" a los nodos que faltan
todos_nodos_categorizados = [nodo for categoria in categorias.values() for nodo in categoria]
nodos_sin_categoria = [nodo for nodo in G.nodes() if nodo not in todos_nodos_categorizados]
if nodos_sin_categoria:
    categorias["Otros"] = nodos_sin_categoria

# Crear diccionario para asignar categoría a cada nodo
nodo_a_categoria = {}
for categoria, nodos_categoria in categorias.items():
    for nodo in nodos_categoria:
        nodo_a_categoria[nodo] = categoria

# Crear figura grande con fondo blanco
plt.figure(figsize=(22, 18), facecolor='white')

# Definir coordenadas específicas para un layout más controlado
pos = {}

# Coordenadas para el nodo raíz
pos["Perros"] = np.array([0, 0])

# Definir posiciones de las categorías principales en un círculo alrededor de "Perros"
categorias_principales = ["Salud", "Alimentación", "Higiene", "Ejercicio", 
                          "Comportamiento", "Entrenamiento", "Cuidados generales", "Razas"]
radio_principal = 6
angulos_principales = np.linspace(0, 2*np.pi, len(categorias_principales), endpoint=False)
angulos_principales = np.roll(angulos_principales, 2)  # Rotar para mejor distribución

for i, categoria in enumerate(categorias_principales):
    pos[categoria] = np.array([radio_principal * np.cos(angulos_principales[i]), 
                               radio_principal * np.sin(angulos_principales[i])])

# Función para posicionar nodos secundarios alrededor de su nodo padre
def posicionar_nodos_secundarios(padre, hijos, radio=3.0, angulo_inicial=0):
    if not hijos:
        return
    
    # Definir ángulos para los hijos
    angulos = np.linspace(angulo_inicial, angulo_inicial + 2*np.pi/3, len(hijos), endpoint=False)
    
    # Obtener posición del padre
    padre_pos = pos[padre]
    
    # Posicionar cada hijo
    for i, hijo in enumerate(hijos):
        if hijo not in pos:  # Evitar sobreescribir posiciones ya definidas
            angulo = angulos[i]
            pos[hijo] = np.array([padre_pos[0] + radio * np.cos(angulo), 
                                  padre_pos[1] + radio * np.sin(angulo)])

# Para cada categoría principal, posicionar sus hijos directos
for padre in categorias_principales:
    hijos = [hijo for origen, hijo in nodos if origen == padre]
    # Calcular ángulo según la posición del padre respecto al centro
    angulo_padre = np.arctan2(pos[padre][1], pos[padre][0])
    posicionar_nodos_secundarios(padre, hijos, radio=2.5, angulo_inicial=angulo_padre - np.pi/6)

# Para cada nodo secundario, posicionar sus hijos terciarios
for origen, destino in nodos:
    if origen not in categorias_principales and origen != "Perros":
        hijos = [hijo for origen2, hijo in nodos if origen2 == origen]
        if origen in pos:  # Asegurarse de que el origen ya tiene posición
            angulo_origen = np.arctan2(pos[origen][1] - pos.get(padre, np.array([0, 0]))[1], 
                                       pos[origen][0] - pos.get(padre, np.array([0, 0]))[0])
            posicionar_nodos_secundarios(origen, hijos, radio=2.0, angulo_inicial=angulo_origen)

# Para los nodos que aún no tienen posición, usar spring_layout 
nodos_sin_posicion = [nodo for nodo in G.nodes() if nodo not in pos]
if nodos_sin_posicion:
    subgrafo = G.subgraph(nodos_sin_posicion)
    pos_temp = nx.spring_layout(subgrafo, k=2.0)
    
    # Ajustar las posiciones para que no se solapen con las existentes
    max_existente_x = max([p[0] for p in pos.values()])
    max_existente_y = max([p[1] for p in pos.values()])
    
    for nodo, posicion in pos_temp.items():
        pos[nodo] = np.array([posicion[0] + max_existente_x + 5, posicion[1] + max_existente_y])

# Definir colores para cada categoría
colores_categorias = {
    "Raíz": "#3498db",        # Azul claro
    "Salud": "#e74c3c",       # Rojo
    "Alimentación": "#2ecc71", # Verde
    "Higiene": "#f39c12",     # Amarillo/Naranja
    "Ejercicio": "#9b59b6",   # Morado
    "Comportamiento": "#1abc9c", # Verde azulado
    "Entrenamiento": "#e84393", # Rosa
    "Cuidados generales": "#7f8c8d", # Gris
    "Razas": "#f1c40f",       # Amarillo
    "Otros": "#95a5a6"        # Gris claro
}

# Preparar los colores y tamaños de nodos según su categoría y relevancia
node_colors = [colores_categorias[nodo_a_categoria[nodo]] for nodo in G.nodes()]
node_sizes = []

for nodo in G.nodes():
    if nodo == "Perros":
        node_sizes.append(2000)  # Nodo raíz más grande
    elif nodo in categorias_principales:
        node_sizes.append(1600)  # Categorías principales grandes
    elif nodo in ["Síntomas de emergencia", "Vacunas", "Enfermedades comunes", "Esterilización",
                 "Alimentos prohibidos"]:
        node_sizes.append(1300)  # Subcategorías importantes medianas
    else:
        node_sizes.append(1000)  # Resto de nodos más pequeños

# Dibujar nodos con efectos de sombra para mejor visibilidad
nx.draw_networkx_nodes(G, pos, 
                      node_size=node_sizes, 
                      node_color=node_colors,
                      alpha=0.9,
                      edgecolors='black', 
                      linewidths=1)

# Dibujar las etiquetas de los nodos con mejor legibilidad
labels = {node: node for node in G.nodes()}
text_items = nx.draw_networkx_labels(G, pos, labels=labels, 
                                    font_size=9, 
                                    font_weight='bold',
                                    font_family='sans-serif')

# Añadir efectos de contorno blanco a las etiquetas para mejor legibilidad
for text in text_items.values():
    text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground='white')])

# Dibujar las aristas con curvas para evitar superposiciones
curved_edges = []
for edge in G.edges():
    source, target = edge
    source_pos, target_pos = pos[source], pos[target]
    rad = 0.1  # Curvatura de las aristas
    curved_edges.append((source_pos, target_pos, rad))

# Función para dibujar aristas curvas con flechas
def draw_curved_edges(edges, ax, color='gray', alpha=0.7, width=1.5, arrowsize=15):
    for source_pos, target_pos, rad in edges:
        # Crear un objeto FancyArrowPatch con curvatura
        arrow = FancyArrowPatch(
            source_pos, target_pos,
            connectionstyle=f'arc3,rad={rad}',
            arrowstyle='-|>',
            mutation_scale=arrowsize,
            linewidth=width,
            color=color,
            alpha=alpha
        )
        ax.add_patch(arrow)

# Obtener el objeto axes actual
ax = plt.gca()
draw_curved_edges(curved_edges, ax)

# Añadir una leyenda para las categorías
legend_elements = []
for categoria, color in colores_categorias.items():
    if categoria in nodo_a_categoria.values():  # Solo incluir categorías usadas
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', label=categoria,
                              markerfacecolor=color, markersize=10))

plt.legend(handles=legend_elements, loc='upper right', title="Categorías", 
          fontsize=10, title_fontsize=12, bbox_to_anchor=(1.05, 1), frameon=True)

# Ajustar el título y los márgenes
plt.title("Mapa Conceptual de Cuidado Canino", fontsize=20, pad=20)
plt.tight_layout()
plt.axis('off')  # Ocultar ejes

# Guardar la imagen con alta resolución
plt.savefig("cuidado_canino_mejorado.png", dpi=300, bbox_inches="tight", facecolor='white')
plt.savefig("cuidado_canino_mejorado.svg", format='svg', bbox_inches="tight", facecolor='white')

# Mostrar el gráfico
plt.show()