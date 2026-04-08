# Pokemon - Modelado y Seleccion de Modelo

> Proposito: convertir evidencia tecnica en una decision de modelo defendible y reproducible.

Este documento es la transcripcion en espanol del notebook de modelado y seleccion de modelo.

## Objetivos de la fase

1. Establecer una linea base cuantitativa (Dummy, Logistic, Tree).
2. Comparar candidatos de mayor capacidad bajo el mismo protocolo de validacion.
3. Optimizar hiperparametros con Optuna usando F1 como metrica objetivo.
4. Seleccionar el modelo final con criterios explicitos y auditables.
5. Evaluar una sola vez en test hold-out y discutir errores.
6. Persistir artefactos y evidencia tecnica para trazabilidad.

## Preguntas que responde este documento

1. La mejora de modelos complejos frente a baselines es real o aparente?
2. Que aporta el tuning y cuanto mejora efectivamente?
3. El modelo seleccionado generaliza en test de forma consistente con CV?
4. Que tipo de errores comete y como cambia con distintos umbrales?
5. Que variables sostienen la prediccion y son coherentes con EDA?

## Guia de lectura rapida

1. Validez del experimento y contrato tecnico.
2. Comparacion inicial de modelos.
3. Optimizacion y seleccion.
4. Generalizacion y diagnostico.
5. Interpretabilidad y cierre de gobernanza.

## Marco metodologico y criterios de decision

Este flujo sigue una linea metodologica orientada a validez estadistica, comparabilidad entre experimentos y trazabilidad de decisiones.

### Principios metodologicos aplicados

- Reutilizar exactamente el pipeline de preprocesamiento generado en Data Preparation.
- Mantener test completamente aislado hasta la evaluacion final.
- Comparar primero modelos base y luego modelos de mayor capacidad.
- Aplicar el mismo esquema de validacion cruzada estratificada para todos los modelos.
- Registrar resultados y artefactos para reproducibilidad y auditoria.

### Continuidad con EDA y Data Preparation

- EDA mostro que las senales mas fuertes son relativas (especialmente diff_speed y diff_stats_total).
- Data Preparation elimino variables con riesgo de leakage (Winner, WinRate, Wins, n_combats).
- El split se diseno con criterio de dependencia por matchup para reducir contaminacion train-test.
- Modelado parte de esos contratos tecnicos, sin reprocesar datos desde cero.

### Familias de modelos

Modelos base:
- Dummy Classifier.
- Logistic Regression.
- Decision Tree.

Modelos candidatos:
- Random Forest.
- HistGradientBoosting.

### Metricas de evaluacion

Metrica principal:
- F1-score.

Metricas complementarias:
- Accuracy.
- Balanced Accuracy.
- ROC-AUC.

### Regla de avance

Solo pasan a tuning los modelos que:
- superan de forma consistente a los baselines en CV-F1,
- mantienen coherencia en metricas complementarias,
- justifican su complejidad adicional frente a costo computacional.

## Estructura general de un modelo en Scikit-Learn

Patron operativo: definir, entrenar, predecir y opcionalmente estimar probabilidades.

```python
from sklearn.some_module import SomeModel

# 1) Definir el estimador con hiperparametros
model = SomeModel(param1=..., param2=...)

# 2) Entrenar
model.fit(X_train, y_train)

# 3) Predecir
y_pred = model.predict(X_test)

# 4) Opcional: probabilidades
y_proba = model.predict_proba(X_test)[:, 1]
```

En este proyecto, ese patron se encapsula en un pipeline de preprocesamiento + modelo para evitar discrepancias entre entrenamiento e inferencia.

## Importaciones y configuracion

Contrato experimental: mismas reglas para todos los modelos.

Se fija:
- semilla aleatoria para reproducibilidad,
- validacion cruzada estratificada,
- conjunto comun de metricas,
- rutas de salida de reportes y figuras.

## Carga de artefactos preparados

Se cargan artefactos persistidos por Data Preparation:
- split de entrenamiento y prueba,
- pipeline de preprocesamiento,
- manifiesto de variables.

## Validacion estructural

Se verifica:
- objetivo binario correcto,
- misma estructura de columnas entre train y test,
- esquema apto para ejecutar CV y tuning sin fallos estructurales.

## Funciones auxiliares del pipeline

Se definen utilidades para estandarizar entrenamiento y evaluacion:
- construir pipelines homogeneos,
- convertir a denso solo cuando el estimador lo requiere,
- devolver metricas CV con estructura comun.

## Pipeline completo de modelado

Cada experimento sigue el mismo esqueleto:
- preprocess,
- to_dense (condicional),
- model.

## Definicion de modelos base y candidatos

Baselines:
- Dummy,
- Logistic Regression,
- Decision Tree.

Candidatos:
- Random Forest,
- HistGradientBoosting.

## Conclusiones de lineas base

| Modelo base | CV-F1 |
|---|---:|
| Decision Tree | 0.959 |
| Logistic Regression | 0.953 |
| Dummy | 0.000 |

Conclusiones:
- existe senal predictiva real,
- Decision Tree muestra ventaja leve,
- se justifica evaluar ensambles.

## Conclusiones de candidatos

| Modelo candidato | CV-F1 |
|---|---:|
| HistGradientBoosting | 0.972 |
| Random Forest | 0.957 |
| Mejor baseline (Decision Tree) | 0.959 |

Conclusiones:
- HistGradientBoosting lidera pre-tuning,
- Random Forest requiere tuning para escalar,
- ambos pasan a optimizacion.

## Ranking consolidado pre-tuning

| Posicion | Modelo | CV-F1 |
|---:|---|---:|
| 1 | HistGradientBoosting | 0.972 |
| 2 | Decision Tree | 0.959 |
| 3 | Random Forest | 0.957 |
| 4 | Logistic Regression | 0.953 |

## Optimizacion de hiperparametros con Optuna

Criterios de rigor:
- tuning solo sobre train,
- misma CV para todos los trials,
- metrica objetivo CV-F1,
- test aislado.

Separacion aplicada:
- optimizacion de Random Forest en una celda,
- optimizacion de HistGradientBoosting en otra celda.

## Conclusiones de tuning

| Modelo | Antes | Despues | Ganancia |
|---|---:|---:|---:|
| HistGradientBoosting | 0.972 | 0.975 | +0.003 |
| Random Forest | 0.957 | 0.971 | +0.014 |

Lectura:
- HGB mejora por ajuste fino,
- RF recupera competitividad de forma marcada.

## Seleccion final

Regla: maximo CV-F1 bajo protocolo homogeneo.

| Posicion | Modelo | CV-F1 |
|---:|---|---:|
| 1 | HistGradientBoosting tuned | 0.975 |
| 2 | HistGradientBoosting | 0.972 |
| 3 | Random Forest tuned | 0.971 |

## Evaluacion final en test

| Metrica | Valor |
|---|---:|
| Accuracy | 0.979 |
| Balanced Accuracy | 0.979 |
| F1 | 0.978 |
| ROC-AUC | 0.998 |

Lectura:
- desempeno alto y consistente,
- sin degradacion relevante fuera de muestra.

## Diagnostico de errores y umbral

Se analiza:
- matriz de confusion,
- classification report,
- trade-off precision-recall para distintos umbrales.

Nota metodologica:
- el umbral operativo debe fijarse en validacion interna,
- test se usa para confirmacion final.

## Interpretabilidad

Consistencia esperada con EDA:
- mayor peso de diff_speed y diff_stats_total,
- aporte intermedio de diferencias ofensivas,
- aporte marginal de variables con senal cercana al azar.

## Persistencia y gobernanza

Se guardan:
- pipeline final entrenado,
- comparativa de seleccion,
- metricas de test,
- model card.

Esto garantiza trazabilidad, reproducibilidad y continuidad operacional.

## Conclusiones finales

1. Se mantuvo un protocolo homogeneo de comparacion.
2. Los baselines confirmaron senal predictiva real.
3. HistGradientBoosting lidero antes y despues del tuning.
4. Mejor CV-F1: 0.975 (HistGradientBoosting tuned).
5. En test: Accuracy 0.979, F1 0.978, ROC-AUC 0.998.
6. El proceso queda documentado para auditoria y mantenimiento.
