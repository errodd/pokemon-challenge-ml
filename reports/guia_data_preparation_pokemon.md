# Guia actualizada de Data Preparation para Pokemon

## 1. Objetivo de la fase

La fase de data preparation transforma datos crudos en insumos confiables para entrenar modelos sin leakage y con alta reproducibilidad.

Entregables minimos:
- X_train, X_test, y_train, y_test
- preprocess_pipeline (sklearn)
- manifiesto de features y reglas
- artefactos serializados para la siguiente fase

## 2. Unidad de modelado y target

En este proyecto la unidad de modelado es una batalla.

Definicion del target:
- first_wins = 1 si Winner == First_pokemon
- first_wins = 0 en caso contrario

Esto implica que el dataset final debe estar a nivel batalla, no a nivel Pokemon individual.

## 3. Conceptos tecnicos clave

### 3.1 Data leakage

Hay leakage cuando una feature contiene informacion del futuro o del target real de forma directa/indirecta.

Variables que deben excluirse en entrenamiento:
- Winner
- WinRate
- Wins
- n_combats

Razon:
- Winner define el target.
- WinRate/Wins/n_combats derivan de resultados historicos y pueden inyectar informacion del outcome.

### 3.2 Feature engineering relacional

En batallas, el mejor enfoque es modelar diferencias entre oponentes:
- diff_hp = first_HP - second_HP
- diff_speed = first_Speed - second_Speed
- diff_stats_total

Tambien es util usar magnitud de diferencia:
- abs_diff_speed = |diff_speed|

### 3.3 Tratamiento de ausencia estructural

Type 2 no es missing aleatorio: representa ausencia de segundo tipo.
Se recomienda codificarlo explicitamente como "None".

### 3.4 Duplicados y dependencia

Duplicados exactos en combates pueden inflar metricas.
Se deben eliminar antes del split y antes de crear features.

## 4. Estructura profesional recomendada del notebook

1. Imports y configuracion
2. Carga de datos
3. Auditoria minima y reglas anti-leakage
4. Limpieza estructural
5. Funciones de feature engineering
6. Construccion del dataset batalla
7. Target y split temprano
8. Feature selection y tipado
9. Pipeline de preprocessing
10. Validacion tecnica
11. Persistencia de artefactos
12. Output summary

## 5. Funciones clave (que debes dominar)

### 5.1 build_pokedex_lookup

Objetivo:
- Crear una tabla indexada por ID de Pokemon para joins rapidos.
- Agregar stats_total.

Entrada:
- pokemon_df

Salida:
- lookup indexado por #

### 5.2 build_battle_level_dataset

Objetivo:
- Convertir combates en dataset de modelado con features de ambos oponentes.

Incluye:
- target first_wins
- features first_* y second_*
- features diff_* y abs_diff_*
- relaciones: same_type1, same_generation, both_legendary

## 6. Diseño del preprocess pipeline

Separar por tipo de variable:
- Numericas: imputacion mediana
- Categoricas: imputacion moda + OneHotEncoder(handle_unknown="ignore")
- Binarias: passthrough

Implementacion:
- Pipeline por bloque
- ColumnTransformer para componer todo

Regla de oro:
- fit en train
- transform en train y test

## 7. Validaciones tecnicas obligatorias

Antes de pasar a modelado:
- verificar shapes train/test
- verificar balance de target por split
- validar que no existan columnas de leakage
- validar transformacion sin errores
- registrar lista final de features

## 8. Artefactos y reproducibilidad

Guardar:
- preprocess_pipeline_pokemon.joblib
- split_data_pokemon.joblib
- feature_manifest_pokemon.json

Ventajas:
- repetibilidad
- trazabilidad de decisiones
- continuidad limpia con notebook de modelado

## 9. Errores comunes y como evitarlos

1. Hacer feature engineering despues de mezclar train y test
- Solucion: split temprano.

2. Entrenar con columnas de identidad
- Solucion: excluir First_pokemon, Second_pokemon, Name y similares.

3. Usar metricas historicas de outcome como predictors
- Solucion: excluir WinRate/Wins/n_combats.

4. No documentar features finales
- Solucion: crear feature manifest.

5. No deduplicar combates
- Solucion: deduplicar por First_pokemon, Second_pokemon, Winner.

## 10. Checklist rapido de calidad

- El target está bien definido y auditado.
- No hay leakage en X.
- El split es estratificado.
- El pipeline transforma sin romper en test.
- Los artefactos fueron guardados.
- Existe resumen tecnico final con decisiones y limites.

## 11. Que sigue en la fase 3 (modeling)

Siguiente notebook recomendado:
- baseline logistico y arbol
- comparacion con CV
- calibracion de probabilidades
- analisis de errores por subgrupos
- interpretabilidad (feature importance / SHAP segun modelo)

Con esta base, tu fase de modelado parte de un dataset robusto y profesional, alineado con buenas practicas de machine learning aplicado.
