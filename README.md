# Sistema de Análisis de Criptomonedas en Tiempo Real con Inteligencia Artificial

## Introducción y Justificación del Problema a Resolver

En el dinámico y volátil mundo de las criptomonedas, tomar decisiones informadas es crucial para maximizar ganancias y minimizar riesgos. La velocidad a la que cambian los precios y la avalancha de información disponible pueden abrumar tanto a inversores novatos como experimentados. Nuestro proyecto surge para abordar este desafío, ofreciendo un sistema de análisis de criptomonedas en tiempo real potenciado por inteligencia artificial generativa. Buscamos ayudar a las personas a tomar mejores decisiones al comprar criptomonedas, proporcionándoles herramientas y análisis que les permitan aumentar sus ganancias y gestionar sus inversiones de manera más eficiente.

## Descripción del Dataset, Origen y Tamaño de Datos

El sistema maneja dos tipos principales de datos:

1. **Datos en Tiempo Real de Criptomonedas**:
   - **Origen**: APIs de Coinbase y CoinGecko.
   - **Contenido**: Top 10 de criptomonedas con información sobre precio en tiempo real, volumen de transacciones, cambios porcentuales en la última hora, 24 horas y 7 días, capitalización de mercado, entre otras variables.
   - **Tamaño**: Datos continuos y actualizados constantemente, lo que genera un flujo significativo de información.

2. **Noticias Relacionadas con Criptomonedas**:
   - **Fuentes**:
     - **Google News**: Noticias generales y tendencias actuales.
     - **CoinMarketCap News**: Información especializada del mercado cripto.
     - **CryptoFlash News**: Actualizaciones rápidas y relevantes del sector.
   - **Contenido**: Artículos y publicaciones que afectan o reflejan el estado del mercado de criptomonedas.
   - **Tamaño**: Gran volumen de documentos textuales que se actualizan periódicamente.


## Dificultad Técnica

El proyecto presenta varios desafíos técnicos:

- **Manejo de Datos en Tiempo Real**: Capturar, procesar y visualizar datos que cambian constantemente requiere sistemas eficientes y escalables.
- **Implementación de LLMs con RAG**: Integrar modelos de lenguaje (LLMs) con Retrieval Augmented Generation para proporcionar respuestas informadas basadas en las últimas noticias.
- **Scraping Web Eficiente**: Extraer datos de múltiples fuentes web de manera efectiva.

## Herramientas y Tecnologías Empleadas

- **Procesamiento de Datos**:
  - **Modin**: Para acelerar operaciones de pandas en grandes datasets.
- **Streaming y Mensajería**:
  - **Kafka**: Manejo de datos en tiempo real y colas de mensajes.
- **Bases de Datos**:
  - **MongoDB**: Almacenamiento de noticias en formato de documentos.
  - **Bases de Datos SQL**: Para almacenar y gestionar datos estructurados de criptomonedas.
- **Visualización y BI**:
  - **Streamlit**: Creación de dashboards interactivos para visualizar datos y análisis.
- **Inteligencia Artificial**:
  - **GPT-4o-mini**: LLM para análisis y generación de los insights en base a las noticias.
  - **LangChain, LangGraph y LangSmith**: Frameworks para construir aplicaciones impulsadas por LLMs.
- **Scraping Web**:
  - **Playwright (JavaScript)**: Automatización y scraping eficiente de páginas web.
- **Embeddings y Vectorización**:
  - **OpenAI Embeddings**: Vectorización de textos para búsqueda y análisis semántico.

## Indicaciones de Cómo Ejecutar el Proyecto

Para poner en marcha el proyecto, siga estos pasos:

1. **Configuración del Entorno**:
   - Cree un entorno virtual con Conda:

     ```bash
     conda create -n crypto_env python=3.12
     conda activate crypto_env
     ```

   - Instale las dependencias necesarias:

     ```bash
     pip install -r requirements.txt
     ```

     *Nota: Asegúrese de que `requirements.txt` incluye todas las librerías necesarias, como `langchain`, `modin`, `streamlit`, etc.*

2. **Iniciar Kafka y ZooKeeper**:
   - Utilice Docker para ejecutar Kafka y ZooKeeper:

     ```bash
     docker-compose up -d
     ```

     *Nota: Asegúrese de tener un archivo `docker-compose.yml` configurado correctamente.*

3. **Configurar Bases de Datos**:
   - **MongoDB**: Asegúrese de que MongoDB está instalado y en ejecución para almacenar las noticias.
   - **Bases de Datos SQL**: Configure su base de datos preferida (MySQL, PostgreSQL, etc.) para almacenar datos de criptomonedas.

4. **Ejecución del Scraper**:
   - Navegue al directorio del scraper y ejecútelo:

     ```bash
     cd scraper
     node scraper.js
     ```

     *Nota: Requiere Node.js para ejecutar scripts de JavaScript.*

5. **Iniciar el Dashboard**:
   - Ejecute la aplicación Streamlit:

     ```bash
     streamlit run app.py
     ```

6. **Configuración de LLMs y Embeddings**:
   - Configure las credenciales de OpenAI para usar GPT-4 Omini y OpenAI Embeddings.
   - Instale librerías adicionales si es necesario:

     ```bash
     pip install langchain textsplitter langchain-community
     ```

*Nota*: La implementación de Apache Pinot fue considerada para el manejo de bases de datos, pero no se logró implementar por dificultades técnicas.

## Arquitectura del Proyecto

![Diagrama de Arquitectura](ruta/al/diagrama.png)

### Descripción de la Arquitectura

- **Ingesta de Datos en Tiempo Real**:
  - **Kafka** recibe datos de las APIs de Coinbase y CoinGecko.
  - Los datos siguen dos flujos:
    - **Flujo Directo**: Se envían al dashboard para visualización en tiempo real.
    - **Flujo de Almacenamiento**: Se guardan en una base de datos para cálculos e insights adicionales antes de ser visualizados.

- **Scraping y Almacenamiento de Noticias**:
  - **Playwright** extrae noticias de las fuentes mencionadas.
  - Las noticias se almacenan en **MongoDB**.

- **Procesamiento y Análisis**:
  - **Modin** y otras herramientas procesan los datos para generar insights.
  - Se utilizan **OpenAI Embeddings** para vectorizar noticias.

- **Inteligencia Artificial y Chatbot**:
  - Implementación de **RAG** utilizando **LangChain** y **GPT-4 Omini**.
  - El chatbot accede a las noticias vectorizadas para proporcionar respuestas informadas.

## Descripción del Proceso ETL/ELT

Seguimos un enfoque **Extract-Load-Transform (ELT)**:

1. **Extracción (Extract)**:
   - Datos de precios y volúmenes desde las APIs.
   - Noticias mediante scraping web.

2. **Carga (Load)**:
   - Los datos se cargan directamente en Kafka y las bases de datos correspondientes.
   - Las noticias se almacenan en MongoDB.

3. **Transformación (Transform)**:
   - Cálculos y agregaciones para generar insights.
   - Vectorización de textos para análisis semántico y uso en el chatbot.

## Resultados Obtenidos y Análisis de Estos

*Borrador*: Hasta el momento, el sistema ha demostrado ser capaz de:

- Proporcionar visualizaciones en tiempo real de las principales criptomonedas, permitiendo a los usuarios observar tendencias y cambios instantáneamente.
- Ofrecer un chatbot que responde preguntas basadas en las últimas noticias, ayudando a los usuarios a entender eventos que podrían afectar al mercado.
- Generar insights valiosos a partir de los datos almacenados, como predicciones de tendencias y alertas sobre cambios significativos.

## Dificultades Identificadas al Momento de Implementar la Solución

*Borrador*:

- **Integración de Apache Pinot**: No se logró implementar por dificultades técnicas, lo que limitó el manejo óptimo de ciertas consultas en tiempo real.
- **Manejo de Datos en Tiempo Real**: Asegurar la sincronización y consistencia de datos provenientes de múltiples fuentes fue un desafío.
- **Optimización del Chatbot**: Ajustar el rendimiento y relevancia de las respuestas del chatbot requirió iteraciones y pruebas exhaustivas.

## Conclusiones y Posibles Mejoras

*Borrador*:

- **Conclusiones**: El proyecto muestra el potencial de combinar datos en tiempo real y técnicas avanzadas de inteligencia artificial para mejorar la toma de decisiones en inversiones de criptomonedas.
- **Posibles Mejoras**:
  - **Implementación de Apache Pinot u Otras Soluciones**: Para mejorar el manejo de datos en tiempo real y consultas complejas.
  - **Ampliación de Fuentes de Datos**: Incluir más APIs y fuentes de noticias para enriquecer el análisis.
  - **Optimización del Chatbot**: Integrar modelos más avanzados y personalizar respuestas según el perfil del usuario.
  - **Mejora en la Visualización**: Incorporar gráficos más interactivos y personalizables en el dashboard.

---

**Nota**: Este documento es un borrador y está sujeto a cambios. Se invita a colaboradores y usuarios a aportar sugerencias y mejoras.

---
