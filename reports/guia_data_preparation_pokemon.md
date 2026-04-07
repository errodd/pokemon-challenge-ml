# Guia actualizada de Data Preparation para Pokemon

## 1. Objetivo de la fase

La fase de Data Preparation convierte datos crudos en insumos entrenables, trazables y libres de leakage.

Entregables tecnicos de esta fase:
- Matrices base para modelado: X_train, X_test, y_train, y_test.
- Pipeline de transformacion reproducible (ColumnTransformer + Pipeline).
- Manifiesto de features con decisiones explicitas (inclusion/exclusion).
- Artefactos persistidos para continuidad directa con modelado.

## 2. Estado actual del notebook (datos relevantes)

Resumen de la ejecucion mas reciente:
- pokemon.csv: 800 filas, 12 columnas.
- combats.csv: 50,000 filas, 3 columnas.
- Combates tras deduplicacion exacta: 48,048.
- Duplicados removidos: 1,952 (3.90%).
- Cobertura de IDs de combate en Pokedex: 100.0%.

Split por dependencia (GroupShuffleSplit con matchup_key):
- Train: 38,429 filas.
- Test: 9,619 filas.
- Media del target en train: 0.4717.
- Media del target en test: 0.4727.
- Solapamiento de grupos entre train/test: 0.

Espacio de features final:
- X_train_final: (38,429, 54).
- X_test_final: (9,619, 54).
- Features numericas: 26.
- Features categoricas: 8.
- Features binarias: 8.
- Entradas en drop_cols: 5 (incluye "Winner" repetido por construccion de lista).

Espacio transformado por el preprocess pipeline:
- Train transformado: (38,429, 481).
- Test transformado: (9,619, 481).

## 3. Unidad de modelado y definicion del target

La unidad de modelado es la batalla, no el Pokemon individual.

Definicion del target:
- first_wins = 1 si Winner == First_pokemon.
- first_wins = 0 en caso contrario.

Implicacion metodologica:
- Las features deben representar ventaja relativa entre contendientes.
- No basta con atributos aislados de un solo Pokemon.

## 4. Conceptos clave explicados

### 4.1 Leakage de datos

Hay leakage cuando una variable contiene informacion del resultado real de forma directa o indirecta.

Variables prohibidas como predictores:
- Winner.
- WinRate.
- Wins.
- n_combats.

Por que:
- Winner define el target directamente.
- WinRate/Wins/n_combats se derivan del historial de resultados y contaminan la validacion.

### 4.2 Leakage por dependencia entre muestras

No todo leakage viene de columnas. Tambien existe leakage por dependencia estructural:
- si el mismo emparejamiento (o muy parecido) cae en train y test,
- el rendimiento en test puede quedar inflado.

Mitigacion aplicada:
- split por grupos usando matchup_key (par no ordenado First/Second).
- validacion explicita: group_overlap = 0.

### 4.3 Feature engineering relacional

La señal se modela como comparacion entre rivales:
- diff_*: direccion y magnitud signed de ventaja.
- abs_diff_*: intensidad de diferencia sin direccion.
- first_has_adv_*: bandera binaria de ventaja del primer Pokemon.

Ejemplos:
- diff_speed = first_Speed - second_Speed.
- abs_diff_speed = |diff_speed|.
- first_has_adv_speed = 1 si diff_speed > 0.

### 4.4 Ausencia estructural en Type 2

Type 2 no se trata como missing aleatorio.

Regla aplicada:
- Type 2 nulo se codifica como "None".

Esto preserva semantica: "no tiene segundo tipo".

### 4.5 Duplicados exactos

Deduplicar combates antes del split reduce dependencia artificial y mejora validez fuera de muestra.

En esta corrida:
- 1,952 filas duplicadas removidas.

## 5. Flujo actualizado del notebook

1. Setup e imports:
- Define RANDOM_STATE = 29 y parametros globales compartidos.

2. Carga de datos:
- pokemon.csv y combats.csv con verificacion inicial de estructura.

3. Auditoria minima:
- valida columnas requeridas,
- declara columnas de leakage,
- verifica cobertura de IDs (100%).

4. Limpieza estructural:
- deduplica combates,
- normaliza Type 2,
- crea is_mega,
- convierte Legendary a entero.

5. Construccion de dataset batalla:
- join first_* y second_*,
- crea target first_wins,
- crea matchup_key,
- genera features relacionales y de interaccion.

6. Split por grupos:
- GroupShuffleSplit por matchup_key,
- evita dependencia train-test por emparejamiento.

7. Seleccion y tipado de features:
- elimina columnas de identidad y leakage,
- organiza en numericas/categoricas/binarias,
- persiste rationale en feature_decisions.

8. Resolucion de preguntas de EDA (Q1/Q2/Q3):
- Q1: entrenabilidad estructural.
- Q2: señales relevantes train-only.
- Q3: exclusion efectiva de variables descriptivas contaminantes.

9. Preprocesamiento reproducible:
- numericas: imputacion por mediana,
- categoricas: moda + one-hot,
- binarias: passthrough.

10. Validaciones tecnicas:
- consistencia de formas,
- target binario,
- transformacion sin errores.

11. Persistencia de artefactos:
- preprocess_pipeline_pokemon.joblib,
- split_data_pokemon.joblib,
- feature_manifest_pokemon.json.

## 6. Señales mas relevantes detectadas (train-only)

Top de señales relacionales por AUC orientado y correlacion con first_wins:
- first_has_adv_speed: AUC 0.9412, corr 0.8814.
- diff_speed: AUC 0.9256, corr 0.6773.
- diff_stats_total: AUC 0.7738, corr 0.4713.
- diff_attack: AUC 0.7090, corr 0.3618.
- diff_sp_atk: AUC 0.7036, corr 0.3508.

Lectura:
- Confirma la narrativa de EDA: la velocidad relativa domina,
- seguida por ventaja total de stats y diferencias ofensivas.

## 7. Discusiones y aclaraciones metodologicas

### 7.1 "Si ya quito Winner, por que hablar de leakage?"

Porque leakage tambien aparece por dependencia de muestras.
Por eso se usa split por matchup_key y no un split aleatorio simple.

### 7.2 "Type 2 faltante no deberia imputarse con moda?"

No en este caso.
Aqui representa una ausencia real de segundo tipo, no un valor perdido por error.

### 7.3 "drop_cols muestra 5 entradas pero no 5 columnas unicas"

Es correcto.
En el manifiesto, "Winner" aparece dos veces por la forma de construir la lista.
No afecta el resultado porque el drop se hace con errors="ignore" y el dataframe final queda consistente.

### 7.4 "Por que hay 54 columnas antes de transformar y 481 despues?"

Porque OneHotEncoder expande categoricas de baja cardinalidad en multiples columnas binarias.
Esa expansion es esperada y controlada por el pipeline.

### 7.5 "Este split reemplaza validacion cruzada?"

No.
Este split prepara train/test limpio para evaluacion final.
La comparacion robusta entre modelos se hace en modelado con CV sobre train.

## 8. Artefactos y contrato con la fase de modelado

Archivos persistidos:
- preprocess_pipeline_pokemon.joblib.
- split_data_pokemon.joblib.
- feature_manifest_pokemon.json.

Que garantiza este contrato:
- reproducibilidad tecnica entre notebooks,
- trazabilidad de decisiones,
- desacople entre preparacion y entrenamiento.

## 9. Errores comunes y como evitarlos

1. Hacer feature engineering despues de mezclar train y test.
Solucion: split temprano por grupos.

2. Mantener columnas de identidad en el set entrenable.
Solucion: excluir First_pokemon, Second_pokemon, Winner, matchup_key.

3. Incluir variables target-derived por "mejorar metrica".
Solucion: prohibir WinRate/Wins/n_combats en features.

4. No documentar por que se elige cada grupo de variables.
Solucion: persistir feature_decisions en el manifiesto.

5. No validar integridad de join.
Solucion: chequeo explicito de filas con mapeo incompleto.

## 10. Checklist de cierre de la fase

- Target binario validado en train y test.
- group_overlap = 0.
- Sin columnas de leakage en X_train_final/X_test_final.
- Pipeline ajusta en train y transforma test sin errores.
- Shapes transformadas consistentes entre train y test.
- Artefactos guardados y versionables.

## 11. Recomendaciones para la fase de modelado

Siguiente paso sugerido:
- comparar baselines y candidatos con CV estratificada,
- mantener F1 como metrica principal,
- preservar test como evaluacion final unica,
- apoyar interpretabilidad en las señales relacionales fuertes identificadas.

Con este Data Preparation, la fase de modelado parte de una base metodologicamente robusta, reproducible y defendible en presentacion tecnica.
