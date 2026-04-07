# Guion resumido para presentacion (PowerPoint)

## Objetivo de este archivo
Documento corto para construir diapositivas claras y guiar la exposicion.

Formato sugerido:
- 10 a 12 diapositivas,
- 8 a 12 minutos,
- lenguaje simple y orientado a decisiones.

## Slide 1 - Titulo y problema
Titulo: "Seleccion de modelo para prediccion de ganador"

Mensaje clave:
- Es un problema de clasificacion binaria.
- Queremos un modelo que generalice, no solo que ajuste train.

Speaker note:
"Aunque el contexto sea Pokemon, el enfoque es el mismo de cualquier problema tabular de clasificacion".

## Slide 2 - Objetivo y criterios de exito
- Objetivo: seleccionar el mejor modelo bajo protocolo reproducible.
- Metrica principal: F1.
- Metricas de apoyo: Accuracy, Balanced Accuracy, ROC-AUC.

Speaker note:
"F1 es central porque balancea precision y recall".

## Slide 3 - Metodo (pipeline)
- Reutilizacion de artefactos de Data Preparation.
- CV estratificada para todos los modelos.
- Test aislado hasta el final.

Speaker note:
"Mismas reglas para todos, comparacion justa".

## Slide 4 - Modelos evaluados
Baselines:
- Dummy
- Logistic Regression
- Decision Tree

Candidatos:
- Random Forest
- HistGradientBoosting

Speaker note:
"Baselines para piso tecnico; candidatos para capturar no linealidad".

## Slide 5 - Ranking pre-tuning
Mostrar tabla corta (top):
- HistGradientBoosting
- DecisionTree
- RandomForest
- LogisticRegression
- Dummy

Mensaje:
- Se observa mejora clara sobre baselines.
- Solo lideres pasan a tuning.

## Slide 6 - Que hace Optuna
- Optimiza hiperparametros en train con CV.
- No toca test.
- Busca mejorar generalizacion.

Speaker note:
"No cambia el tipo de modelo, mejora su configuracion".

## Slide 7 - Resultado de tuning y seleccion
- hist_gradient_boosting_tuned: 0.9731 CV-F1
- random_forest_tuned: 0.9679 CV-F1

Decision:
- Modelo final: hist_gradient_boosting_tuned

## Slide 8 - Resultado final en test
- Accuracy: 0.9760
- Balanced Accuracy: 0.9759
- F1: 0.9746
- ROC-AUC: 0.9973

Mensaje:
- Desempeno alto y consistente fuera de muestra.

## Slide 9 - Diagnostico y umbral
- Reporte por clase + matriz de confusion.
- Analisis de umbral para ajustar precision/recall segun costo de error.

Mensaje:
- El modelo no solo se evalua; tambien se adapta a objetivo operativo.

## Slide 10 - Interpretabilidad
- Importancia global de variables.
- Validacion de coherencia con EDA.

Mensaje:
- Entendemos por que el modelo decide, no solo cuanto acierta.

## Slide 11 - Gobernanza y artefactos
Se guarda:
- pipeline final,
- resultados de seleccion,
- metricas de test,
- model card.

Mensaje:
- Esto habilita auditoria, mantenimiento y despliegue responsable.

## Slide 12 - Cierre: limites y siguientes pasos
Limites:
- falta dispersion por fold,
- umbral a validar fuera de test,
- interpretabilidad local pendiente.

Siguientes pasos:
- calibracion,
- analisis por subgrupos,
- monitoreo de drift,
- prueba de modelos adicionales.

Cierre verbal:
"Se selecciono el mejor modelo bajo un proceso reproducible y explicable; el siguiente paso es fortalecer robustez operativa".

## Checklist rapido antes de presentar
1. Verificar que las metricas del slide coincidan con `reports/pokemon_test_metrics.json`.
2. Incluir tabla corta de ranking desde `reports/pokemon_model_selection_results.csv`.
3. Mostrar al menos una figura: matriz de confusion o importancia de variables.
4. Ensayar explicacion de F1 en 15 segundos.
5. Cerrar con limites y plan de mejora (muestra madurez tecnica).
