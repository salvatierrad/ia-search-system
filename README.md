# Sistema de Búsqueda Semántica con LangChain y LanceDB

Este proyecto implementa un sistema de búsqueda semántica interactivo que usa **LangChain** y **LanceDB** para responder preguntas basadas en un conjunto de frases, con enfoque en IA y medicina. Convierte las frases en embeddings, las almacena en LanceDB, y usa similitud coseno para devolver respuestas relevantes, reconociendo sinónimos y conceptos relacionados. Permite añadir nuevas frases dinámicamente, que se guardan de forma persistente, y detecta preguntas no relevantes.

## Cómo instalar

1. Clona este repositorio:

   ```bash
   git clone https://github.com/salvatierrad/ia-search-system
   cd ia-search-system
   ```
2. Crea un entorno virtual e instala las dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecuta el programa:

   ```bash
   python main.py
   ```

## Qué hace

- Carga frases iniciales sobre IA y medicina.
- Genera embeddings con LangChain y HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`).
- Almacena los embeddings en LanceDB (en `./my_lancedb`).
- Permite hacer preguntas y añadir nuevas frases desde la consola, con persistencia entre sesiones.
- Usa búsqueda semántica para reconocer sinónimos y conceptos relacionados (por ejemplo, "asiste" y "ayuda", o "médicos" y "doctores").
- Responde con las frases más similares (similitud ≥ 0.5) o indica si no entiende la pregunta.

## Ejemplo

1. Hacer una pregunta:
   - Pregunta: "Cómo asiste la IA a los médicos?"
   - Respuesta: "La inteligencia artificial ayuda a los doctores a diagnosticar enfermedades. (Similitud: 0.90)"
2. Pregunta no relevante:
   - Pregunta: "Qué es un dinosaurio?"
   - Respuesta: "No entiendo tu pregunta o no tengo información relevante."
3. Añadir una frase:
   - Nueva frase: "La IA asiste en la detección de fracturas óseas mediante imágenes médicas."
   - Pregunta: "Cómo ayuda la IA con fracturas?"
   - Respuesta: "La IA asiste en la detección de fracturas óseas mediante imágenes médicas. (Similitud: 0.91)"

## Autor

Diego Salvatierra
