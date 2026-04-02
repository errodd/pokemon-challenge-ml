# Critica tecnica del Data Preparation (Pokemon)

## Alcance de la revision

Se reviso:
- claridad del texto y orden narrativo,
- utilidad practica para modelado,
- impacto metodologico sobre validez del modelo,
- coherencia con hallazgos del EDA,
- alineacion estructural con el ejemplo de Titanic.

Archivos revisados:
- notebooks/Data Preparation.ipynb
- notebooks/EDA.ipynb
- 02_data_preparation.ipynb
- reports/guia_data_preparation_pokemon.md

## Hallazgos principales (priorizados)

### 1) Riesgo critico detectado y corregido: split no dependency-aware

Observacion original:
- El split estratificado simple no controlaba emparejamientos repetidos entre train y test.

Impacto:
- Riesgo de sobreestimar performance por dependencia entre muestras.

Correccion aplicada en version ajustada:
- Se implemento `matchup_key` (pareja no ordenada) y `GroupShuffleSplit` para separar por grupos.
- Se agrego chequeo explicito de solapamiento de grupos (debe ser 0).

### 2) Riesgo alto detectado y corregido: falta de validacion de joins

Observacion original:
- El ensamblado por ID podia introducir filas incompletas sin detener el flujo.

Impacto:
- NaNs silenciosos en features criticas y degradacion del entrenamiento.

Correccion aplicada:
- Se agrego control post-join con `raise ValueError` si existen filas sin mapeo.

### 3) Mejora de coherencia EDA -> Data Preparation

Observacion original:
- El EDA advertia riesgo por dependencias en validacion, pero no estaba totalmente operacionalizado en preparation.

Impacto:
- Desalineacion entre evidencia exploratoria y protocolo de modelado.

Correccion aplicada:
- Split dependency-aware incorporado.
- Resumen final actualizado con trazabilidad de decisiones metodologicas.

### 4) Mejora de reproducibilidad transversal

Observacion original:
- Semilla distinta entre EDA y Data Preparation.

Impacto:
- Menor comparabilidad entre fases.

Correccion aplicada:
- `RANDOM_STATE` alineado con EDA.

### 5) Estandarizacion de rutas de artefactos

Observacion original:
- Ruta de artefactos local al notebook podia dispersar outputs.

Impacto:
- Friccion operativa al encadenar notebooks.

Correccion aplicada:
- Artefactos persistidos en `../artifacts` para consistencia de proyecto.

## Evaluacion de claridad y utilidad

Fortalezas:
- Estructura seccional limpia y pedagogica.
- Definicion clara de target y anti-leakage.
- Pipeline reproducible con artefactos y manifiesto de features.

Oportunidades:
- Incluir una seccion breve de "Decision tomada por evidencia EDA" por cada ajuste importante.
- Incorporar una tabla de "riesgo -> mitigacion" al inicio o cierre.

## Influencia sobre el modelo

Mejoras esperadas con la version ajustada:
- Metricas de validacion mas realistas (menos optimismo por dependencia).
- Menor riesgo de contaminacion por joins incompletos.
- Mayor robustez metodologica para comparacion de modelos en fase 3.

Trade-off tecnico:
- El split por grupos puede generar ligeras variaciones en balance de clases frente a un split estratificado puro, pero mejora validez de generalizacion.

## Relacion con el EDA

Alineaciones fuertes:
- Unidad de modelado a nivel batalla.
- Exclusiones por leakage (`Winner`, `WinRate`, `Wins`, `n_combats`).
- Tratamiento estructural de `Type 2`.
- Gestion de duplicados.

Alineacion reforzada en ajuste:
- Riesgo de dependencia en validacion traducido a implementacion concreta (Group split).

## Alineacion con la estructura del ejemplo Titanic

La estructura se mantiene alineada al patron del ejemplo:
1. imports/configuracion
2. carga
3. auditoria
4. limpieza
5. feature engineering
6. split
7. seleccion/tipado
8. pipeline
9. validacion
10. persistencia
11. output summary

Diferencia positiva:
- Se agregan controles especificos del dominio de batallas (matchup grouping e integridad de joins), ausentes en Titanic por naturaleza del dataset.

## Estado final

La version ajustada queda metodologicamente mas solida, mejor conectada con el EDA y con mejor validez para la fase de modelado.

## 14) Guia rapida de estudio (resumen)
Conceptos tecnicos que debes dominar para esta fase:
- Unidad de analisis: una fila = una batalla.
- Variable objetivo: `first_wins`.
- Leakage: cualquier variable derivada de resultados historicos globales.
- Feature engineering relacional: modelar diferencias entre oponentes (`diff_*`).
- Validacion dependency-aware: evitar que el mismo emparejamiento aparezca en train y test.
- Preprocessing por tipo: numericas, categoricas, binarias.
- Reproducibilidad: versionado, pipeline serializado y manifiesto de features.

Para estudio extendido, consulta el archivo `reports/guia_data_preparation_pokemon.md`.