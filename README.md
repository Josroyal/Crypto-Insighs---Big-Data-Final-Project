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

## Indicaciones para Ejecutar el Proyecto

### 1. **Configuración del Entorno**:
   - Cree un entorno virtual con Conda:
     ```bash
     conda create -n bigdata_llm python=3.11.7
     conda activate bigdata_llm
     ```
   - Instale las dependencias necesarias:
     ```bash
     pip install -r requirements.txt
     ```
     *Nota*: Verifique que el archivo `requirements.txt` incluya librerías como `langchain`, `modin`, `streamlit`, `kafka-python`, entre otras necesarias.

### 2. **Iniciar Kafka y ZooKeeper**:
   - Configure y arranque Kafka y ZooKeeper con Docker. Use los siguientes comandos:
     - Cree una red para Kafka:
       ```bash
       docker network create kafka-net
       ```
     - Asegúrese de que no haya contenedores anteriores ejecutándose:
       ```bash
       docker rm -f zookeeper kafka
       ```
     - Ejecute los servicios de ZooKeeper y Kafka en terminales separadas:
       - ZooKeeper:
         ```bash
         docker run --name zookeeper --network kafka-net -p 2181:2181 -d zookeeper
         ```
       - Kafka:
         ```bash
         docker run -p 9092:9092 --name kafka --network kafka-net -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -d confluentinc/cp-kafka
         ```

### 3. **Configurar Bases de Datos**:
   - **MongoDB**: Asegúrese de que MongoDB está configurado y ejecutándose para almacenar datos relacionados con noticias y análisis.
   - **SQL Databases**: Configure su base de datos SQL (MySQL o PostgreSQL) para manejar datos estructurados, como precios y métricas de criptomonedas.

### 4. **Ejecución del Scraper**:
   - Navegue al directorio donde está el scraper:
     ```bash
     cd scraper
     ```
   - Ejecútelo con Node.js:
     ```bash
     node scraper.js
     ```

#### 5. **Iniciar el Dashboard**:
   - Inicie la aplicación de visualización con Streamlit:
     ```bash
     streamlit run app.py
     ```

### 6. **Configuración de Modelos de Lenguaje y Embeddings**:
   - Configure las credenciales para OpenAI GPT-4 Omni y embeddings.
   - Instale librerías necesarias adicionales:
     ```bash
     pip install langchain langchain-text-splitters langchain-community
     ```
   - *Siga el tutorial de RAG en LangChain para implementar Recuperación con Generación*:
     [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/).

#### 7. **Alternativas Consideradas**:
   - **Apache Pinot**: Se evaluó para el manejo de datos de alta frecuencia, pero no se implementó debido a limitaciones técnicas.
   - **Tutorial de Coinbase API**: Consulte cómo obtener precios spot de criptomonedas usando su API:
     [StackOverflow - Coinbase API](https://stackoverflow.com/questions/70868199/coinbase-api-call-to-get-crypto-spot-prices).

---

### Observaciones Adicionales
- Considere integrar todas las librerías (`modin`, `streamlit`, `kafka-python`, etc.) en el entorno `bigdata_llm` para simplificar la administración de dependencias.
- Si necesita ajustar los detalles de configuración, puede agregar scripts auxiliares o usar archivos de configuración YAML para centralizar parámetros.

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
