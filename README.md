# Impacto del ENSO en los Índices de Precipitación y Temperatura Extrema en la Región de La Plata 🌊🌡️
**Proyecto Final de Tecnologias Aplicadas para Business Intelligence (TABI)**

## 🎯 Resumen del Proyecto
Este repositorio contiene una solución integral de **Business Intelligence** diseñada para monitorear y analizar la influencia del fenómeno **El Niño–Oscilación del Sur (ENSO)** sobre los extremos climáticos en la región de La Plata. 

El valor principal de este trabajo radica en la **integración de fuentes heterogéneas** dentro de un **modelo dimensional** orientado a la toma de decisiones.

## 🏗️ Ingeniería y Arquitectura de Datos
A diferencia de un análisis exploratorio convencional, aquí se aplicaron principios de BI para estructurar la información:

- **Fuentes de Datos:**
  - 🌐 **Globales (NOAA):** Índices ONI, SOI y MEI para la clasificación de fases ENSO.
  - 📍 **Locales (SMN):** Series diarias procesadas para obtener índices **ETCCDI** (Rx1day, CDD, R99pTOT, etc.).
- **Modelo Dimensional (Esquema en Estrella):**
  - **Tabla de Hechos:** Centraliza las métricas de extremos climáticos por periodo.
  - **Dimensiones:** Jerarquías temporales (años, estaciones) y dimensión ENSO (Fase: Niño/Niña, Intensidad: Débil a Fuerte).



## 🛠️ Stack Tecnológico
- **Procesamiento ETL:** `Python` (`Pandas`, `NumPy`)
- **Motor de Datos:** `DuckDB`
- **Visualización:** `Streamlit` (Dashboard Interactivo)
- **Metodología:** Estándares internacionales **ETCCDI** para detección de cambio climático.

## 📊 Portal Interactivo e Insights
El proyecto incluye un dashboard que permite explorar:
1. **Correlación de Fases:** Impacto visual de El Niño vs. La Niña en la intensidad de las lluvias.
2. **Análisis Estacional:** Variación de extremos térmicos y hídricos según la estación del año.
3. **Soporte de Decisiones:** Información procesada útil para planificación urbana y gestión del riesgo hídrico en la ciudad.

---
**Materia:** Tecnologías Aplicadas al Business Intelligence (TABI)  
**Facultad de Informática - Universidad Nacional de La Plata (UNLP)**