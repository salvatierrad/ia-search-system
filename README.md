# Sistema de Búsqueda Semántica con LangChain y LanceDB

Este proyecto implementa un sistema de búsqueda semántica interactivo que usa **LangChain** y **LanceDB** para responder preguntas basadas en un conjunto de frases, con enfoque en IA y medicina. Convierte las frases en embeddings, las almacena en LanceDB (en `./my_lancedb`), y usa similitud coseno para devolver respuestas relevantes, reconociendo sinónimos y conceptos relacionados. Permite añadir nuevas frases dinámicamente, que se guardan de forma persistente, y detecta preguntas no relevantes.

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

## Ideas de Escalabilidad
Para hacer este sistema más robusto y versátil, se pueden implementar las siguientes mejoras, ampliando su capacidad para manejar grandes volúmenes de datos y diversos formatos de entrada, manteniendo la eficiencia de la búsqueda semántica:

1. **Carga de Archivos de Texto (.txt) por Temas**:
   - **Objetivo**: En lugar de añadir frases individuales, permitir al usuario cargar un archivo `.txt` con información extensa sobre un tema (por ejemplo, un documento sobre "Aplicaciones de IA en cardiología").
   - **Cómo lograrlo**: Leer el archivo `.txt` y dividirlo en fragmentos manejables (por párrafos o oraciones) para generar embeddings. Estos fragmentos se almacenan en LanceDB, asociados con metadatos que indiquen el tema o la fuente. Cuando el usuario hace una pregunta, el sistema busca en los embeddings de los fragmentos y devuelve los más relevantes, concatenando la información en una respuesta coherente.
   - **Librerías clave**:
     - **`os` y `pathlib`**: Para manejar la lectura de archivos `.txt` desde el sistema de archivos.
     - **`langchain.text_splitter` (RecursiveCharacterTextSplitter)**: Para dividir el texto en fragmentos optimizados (por ejemplo, de 500 caracteres con solapamiento), preservando el contexto semántico.
     - **`sentence-transformers`**: Para generar embeddings de los fragmentos, usando el mismo modelo (`all-MiniLM-L6-v2`) o uno más avanzado como `all-mpnet-base-v2` para mayor precisión.
     - **`lancedb`**: Para almacenar los embeddings y metadatos (por ejemplo, nombre del archivo o tema), permitiendo búsquedas vectoriales rápidas.
   - **Beneficios**: Escala el sistema para manejar documentos largos, permite búsquedas temáticas, y mejora la experiencia del usuario al procesar información masiva.

2. **Procesamiento de Archivos CSV con Datos Estructurados**:
   - **Objetivo**: Permitir cargar un archivo `.csv` (por ejemplo, con columnas como "Diagnóstico", "Tratamiento", "Tecnología") y responder preguntas basadas en su contenido (por ejemplo, "¿Qué tratamientos usa la IA para diabetes?").
   - **Cómo lograrlo**: Leer el `.csv` y convertir sus filas o celdas relevantes en texto para generar embeddings. Cada fila se trata como un "documento" con metadatos (como el número de fila o valores de otras columnas). Los embeddings se almacenan en LanceDB, y las preguntas del usuario activan una búsqueda semántica en estos datos. Para mejorar la precisión, se puede combinar la búsqueda vectorial con filtros de metadatos (por ejemplo, buscar solo en filas donde "Diagnóstico = Diabetes").
   - **Librerías clave**:
     - **`pandas`**: Para leer y manipular `.csv`, extrayendo columnas específicas o combinando celdas en texto narrativo.
     - **`langchain.text_splitter`**: Para dividir el texto extraído de las filas en fragmentos si es necesario.
     - **`sentence-transformers`**: Para generar embeddings de los textos derivados del `.csv`.
     - **`lancedb`**: Para almacenar los embeddings con metadatos (por ejemplo, valores de columnas del `.csv`), y soportar búsquedas filtradas.
     - **`numpy`**: Para manejar operaciones vectoriales adicionales, como normalización, si se optimizan embeddings.
   - **Ventajas**: Permite integrar datos estructurados (como bases de datos médicas) en el sistema, ampliando su aplicabilidad a casos de uso como análisis de datos clínicos.

3. **Soporte para Otros Formatos (PDF, Bases de Datos)**:
   - **Objetivo**: Ampliar la entrada a documentos PDF (por ejemplo, artículos científicos) o bases de datos SQL, permitiendo preguntas sobre su contenido.
   - **Cómo lograrlo**: Extraer texto de PDFs o consultar bases de datos, convertir el contenido en fragmentos, generar embeddings, y almacenarlos en LanceDB. Las preguntas del usuario se procesan como en los casos anteriores.
   - **Librerías clave**:
     - **`PyPDF2` o `pdfplumber`**: Para extraer texto de PDFs, manejando formatos complejos (como columnas o tablas).
     - **`sqlalchemy`**: Para conectar a bases de datos relacionales y extraer datos como texto.
     - **`langchain.document_loaders`**: Para cargar diversos formatos (PDF, texto de bases de datos) en el pipeline de LangChain.
     - **`sentence-transformers` y `lancedb`**: Para embeddings y almacenamiento.
   - **Beneficios**: Hace el sistema más versátil, útil para aplicaciones como revisiones bibliográficas o integración con sistemas hospitalarios.

4. **Optimización para Grandes Volúmenes de Datos**:
   - **Objetivo**: Garantizar que el sistema escale a millones de documentos sin perder eficiencia.
   - **Cómo lograrlo**: Usar índices optimizados en LanceDB (como IVF-PQ) para acelerar búsquedas vectoriales. Implementar modelos de compresión de embeddings o usar embeddings dispersos para reducir el almacenamiento. También, paralelizar la generación de embeddings para procesar datos más rápido, aprovechando CUDA si está disponible.
   - **Librerías clave**:
     - **`lancedb`**: Para índices avanzados (IVF-PQ) y almacenamiento eficiente.
     - **`torch`**: Para paralelización en GPU, optimizando la generación de embeddings.
     - **`faiss` (opcional)**: Para búsquedas vectoriales ultra-rápidas en datasets masivos, complementando LanceDB.
     - **Ventajas**: Permite manejar grandes bases de conocimiento, ideal para aplicaciones empresariales.

Estas mejoras transforman el sistema en una plataforma de búsqueda semántica escalable, capaz de procesar diversos formatos y grandes volúmenes de datos, manteniendo su capacidad para responder preguntas con precisión y reconocer sinónimos. La elección de librerías como `pandas`, `PyPDF2`, y `sqlalchemy`, junto con la robustez de `lancedb` y `langchain`, asegura flexibilidad y rendimiento, alineándose con necesidades reales en análisis de datos médicos y de IA.

## Autor
Diego Salvatierra