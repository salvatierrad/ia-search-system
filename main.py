import lancedb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import numpy as np
import torch


# Configurar el modelo para convertir frases en números
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Lista inicial de frases (con temas médicos)
texts = [
    "La inteligencia artificial ayuda a los doctores a diagnosticar enfermedades.",
    "Los modelos de lenguaje procesan grandes cantidades de datos médicos.",
    "LanceDB es una base de datos rápida para buscar información.",
    "La IA detecta osteoporosis en imágenes de rayos X con alta precisión.",
    "Los algoritmos de aprendizaje automático predicen riesgos cardíacos.",
    "LanceDB organiza datos médicos para búsquedas rápidas y eficientes.",
    "La IA mejora la detección temprana de cáncer en mamografías.",
    "Los modelos predictivos identifican pacientes con alto riesgo de diabetes."
]

# Dividir las frases en pedazos pequeños (si son largas)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.create_documents(texts)

# Conectar a LanceDB
db = lancedb.connect("./my_lancedb")

# Crear o abrir la tabla
table_name = "documents"
if table_name not in db.table_names():
    table = db.create_table(
        table_name,
        data=[
            {"text": doc.page_content, "vector": embeddings.embed_query(doc.page_content)}
            for doc in documents
        ],
        mode="append"
    )
else:
    table = db.open_table(table_name)

# Función para calcular la similitud coseno
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Función para añadir una nueva frase
def add_new_phrase(phrase):
    new_doc = text_splitter.create_documents([phrase])[0]
    table.add([{"text": new_doc.page_content, "vector": embeddings.embed_query(new_doc.page_content)}])
    print(f"¡Frase añadida: '{phrase}'!")

# Bucle interactivo
while True:
    print("\nOpciones:")
    print("1. Hacer una pregunta")
    print("2. Añadir una nueva frase")
    print("3. Salir")
    choice = input("Elige una opción (1/2/3): ")

    if choice == "1":
        query = input("Escribe tu pregunta: ")
        query_embedding = embeddings.embed_query(query)
        results = table.search(query_embedding, query_type="vector").limit(2).to_list()

        print("\nPregunta:", query)
        print("Respuesta encontrada:")
        threshold = 0.5  # Umbral de similitud
        found_relevant = False

        for result in results:
            similarity = cosine_similarity(query_embedding, result["vector"])
            if similarity >= threshold:
                print(result["text"], f"(Similitud: {similarity:.2f})")
                found_relevant = True

        if not found_relevant:
            print("No entiendo tu pregunta o no tengo información relevante.")

    elif choice == "2":
        new_phrase = input("Escribe la nueva frase: ")
        add_new_phrase(new_phrase)

    elif choice == "3":
        print("¡Hasta luego!")
        break

    else:
        print("Opción no válida, por favor elige 1, 2 o 3.")