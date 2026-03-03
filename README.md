# research-copilot

# Sección1: "Research Assistant for Judicial Backlash" 

Descripción y temas: Este proyecto consiste en el desarrollo de un Asistente de Investigación basado en Inteligencia Artificial (RAG - Retrieval-Augmented Generation) diseñado para procesar y analizar literatura especializada en ciencia política y derecho constitucional. La herramienta permite la consulta semántica de un corpus de 20 artículos académicos clave que exploran fenómeno como el legalismo autocrático y la colusión de élites, pero especialmente centrado en el tema de el backlash judicial en contextos de regresión democrática.

---

## 2. Features
* **Ingestión Inteligente:** Procesamiento de 20 PDFs académicos con extracción de metadatos bibliográficos.
* **Búsqueda Semántica:** Recuperación de fragmentos basada en similitud de vectores usando `text-embedding-3-small` de OpenAI.
* **Interfaz Multi-página:** Panel central con métricas, sección de chat interactivo, visor de catálogo y análisis de tendencias.
* **Citado Automático:** Generación de respuestas con referencias precisas incluyendo autor, año y título del paper.
* **Dashboard de Métricas:** Visualización de temas únicos, años cubiertos y uso de tokens en tiempo real.

---

## 3. Architecture
El sistema sigue un flujo de tres capas principales:

1.  **Ingestion Pipeline:** Los documentos pasan por una fase de extracción (`PyMuPDF`), limpieza, segmentación (*chunking*) y generación de embeddings.
2.  **Vector Database:** Los vectores se almacenan en **ChromaDB**, manteniendo metadatos clave (autores, años, secciones) vinculados a cada fragmento.
3.  **RAG Pipeline:** La consulta del usuario se vectoriza para recuperar el *top-k* de fragmentos más relevantes, los cuales se inyectan en el prompt del modelo generador (**GPT-4**).

---

## 4. Installation
Para desplegar el proyecto localmente, primero aseguramos el entorno: 

1. **Configuración de entorno:** Cree un archivo `.env` en la raíz con su llave de OpenAI:

```bash
OPENAI_API_KEY=sk-your-key-here
```
   
## 2. Instalación de dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Usage

Para ejecutar la aplicación de escritorio:

```bash
streamlit run app/main.py
```

---

## Consultas de ejemplo

- "¿Cómo definen Meléndez y Perelló la colusión de élites en Guatemala?"
- "¿Qué diferencias existen entre erosión y decaimiento democrático según Gerschewski?"
- "Explica el concepto de legalismo autocrático de Kim Lane Scheppele."

---

## 6. Technical Details

- **Chunking Strategy:** Bloques de 1000 caracteres para mantener la coherencia de los argumentos académicos.  
- **Embedding Model:** `text-embedding-3-small` (OpenAI) por su precisión en textos técnicos.  

### Prompt Engineering Strategies

Implementación de 4 niveles obligatorios:

- **V1:** Instrucciones claras con delimitadores (etiquetas `###`).
- **V2:** Salida en formato JSON estructurado.
- **V3:** *Few-shot prompting* con ejemplos de citas APA.
- **V4:** *Chain-of-thought* para análisis comparativo complejo.

---

## 7. Evaluation Results

| Métrica                | Resultado Estimado                         |
|------------------------|--------------------------------------------|
| Precisión de Citación  | 95% (Base en metadatos de ChromaDB)        |
| Tiempo de Respuesta    | 2.5s - 4.0s (Promedio)                     |
| Relevancia del Contexto| Alta (Top-3 resultados semánticos)         |
| Consumo de Tokens      | ~800 - 1500 por consulta completa          |

---

## 8. Limitations

1. **Papers que puedieron estar dañados:** Por alguna razón, uno de los papers que se estaba empleando no se procesó, lo que ocasionó que solo se trabaje con 19 papers. 

2. **Dependencia de Calidad OCR:** La precisión depende de la capa de texto del PDF; archivos escaneados requieren procesamiento previo adicional.  

3. **Ventana de Contexto:** El sistema recupera un máximo de 5 fragmentos para evitar saturar el límite de tokens y mantener la relevancia del modelo.

## 9. Author Information

1. **Name:** Joverson Reyna

2. **Course Information:** Prompt Engineering usando GPT4 2026-01

3. **Date:** 02, March, 2026


