## 1) Notebook: **01_eda_pokemon_professional**

Solo análisis exploratorio y decisiones (sin transformar dataset final).

1. **Project Context**
    
    - Contexto del problema competitivo Pokémon y objetivo de negocio/ML.
2. **Problem Definition**
    
    - Tarea: clasificación binaria (gana `First_pokemon` vs gana `Second_pokemon`).
3. **Methodological Standard**
    
    - Reproducibilidad, trazabilidad, control de sesgos, no leakage en EDA.
4. **Guiding Principle**
    
    - “Todo análisis debe justificar una decisión posterior”.
5. **Expected Outcomes**
    
    - Qué decisiones esperas cerrar al final del EDA.
6. **Pokemon EDA – Professional Standard**

    - **Objective**
    - **Target** (definición formal de variable objetivo para modelado futuro)
    - **Guiding Questions** (tipo, stats, legendarios, generación, balance, etc.)
7. **Data Audit (sin preparar datos)**

    - Tipos de variables, nulos, duplicados, consistencia IDs entre tablas.
8. **Preliminary Structural Decisions**

    - Decisiones candidatas (qué columnas parecen útiles/no útiles), solo justificación.
9. **Analyzing the Target Variable**

    - Balance de clases (`First_pokemon` gana vs pierde), baseline naive.
10. **Other Analysis (bloques)**

	- Distribución de stats base.
	- Relación stats vs win rate.
	- Tipo 1/Tipo 2 y tasa de victoria.
	- Legendary/Generation vs performance.
	- Interacciones relevantes (ej. Speed × Attack).
11. **Target Analysis – Key Findings**

	- Hallazgos accionables y riesgos para modelado.
12. **Final Preprocessing Decisions (solo diseño, no implementación)**

	- Qué imputar, codificar, escalar, eliminar, agregar.
13. **Executive Technical Summary**
	- Resumen ejecutivo + roadmap del siguiente notebook.

---

## 2) Notebook: **02_data_preparation_pokemon**

Solo preparación de datos (sin modelar).

1. **Objetivo del notebook** y regla anti-leakage.
2. **Split temprano** (train/test).
3. **Construcción de dataset de combates** (joins controlados).
4. **Limpieza e imputación** (solo train-fit).
5. **Codificación de categóricas** (types, legendary, generation).
6. **Escalado/normalización** (si aplica).
7. **Exportar artefactos** (`X_train`, `X_test`, `y_train`, `y_test`, pipeline).

1. **Objetivo de FE** y criterios de aceptación.
2. **Features relacionales por combate** (`diff_attack`, `diff_speed`, ratios, etc.).
3. **Features de matchup de tipos** (ventaja/desventaja).
4. **Features agregadas** (total stats diff, offense/defense indexes).
5. **Control de leakage de features**.
6. **Selección inicial de features** + reporte de importancia preliminar.
7. **Persistencia del set final de features** para modelado.