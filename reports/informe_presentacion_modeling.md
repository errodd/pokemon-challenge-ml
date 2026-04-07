# Informe para Presentacion: Pokemon Model Selection

## 1. Contexto del problema

### a) Problema que se resuelve
Se busca predecir el ganador de una batalla 1v1 entre dos Pokemon usando atributos tabulares del Pokedex y el registro historico de combates.

### b) Tipo de problema
Es un problema de clasificacion binaria:
- Clase 1: gana el primer Pokemon de la fila.
- Clase 0: gana el segundo Pokemon de la fila.

### c) Relevancia del problema
Caso de uso real: en un simulador competitivo, esta prediccion permite apoyar decisiones de alineacion, estimar ventaja previa al combate y priorizar estrategias de enfrentamiento con mejor probabilidad de exito.

## 2. Entendimiento del dataset

### a) Origen del dataset
El proyecto usa dos fuentes del reto:
- Tabla de Pokedex con atributos por Pokemon.
- Bitacora de combates con parejas de Pokemon y ganador observado.

### b) Que representa cada fila
- En pokemon.csv: una fila representa un Pokemon.
- En combats.csv: una fila representa una batalla entre dos Pokemon.

### c) Descripcion general de variables
Resumen estructural:
- pokemon.csv: 799 registros utiles (800 lineas incluyendo encabezado).
- combats.csv: 49,999 batallas utiles (50,000 lineas incluyendo encabezado).

Grupos de variables:
- Numericas base: HP, Attack, Defense, Sp. Atk, Sp. Def, Speed.
- Categoricas: Type 1, Type 2, Generation.
- Binarias: Legendary, is_mega y variables de coincidencia entre rivales.
- Objetivo: first_wins (a nivel batalla).
- Variables excluidas por leakage: Winner, WinRate, Wins, n_combats.

## 3. Principales insights del EDA

### a) Hallazgos relevantes
La señal dominante no viene de variables aisladas, sino de diferencias relativas entre rivales.

señales principales:
- diff_speed: correlacion 0.68 y AUC univariado orientado 0.93.
- diff_stats_total: correlacion 0.47 y AUC 0.77.
- diff_attack y diff_sp_atk: señal adicional relevante.

Interpretacion breve:
- Una correlacion positiva alta indica que, al aumentar la ventaja del primer Pokemon en esa variable, aumenta su probabilidad de ganar.
- El AUC univariado orientado mide que tan bien una sola variable separa victorias y derrotas: 0.93 es señal muy fuerte, mientras 0.77 es buena señal pero de menor poder discriminante.

### b) Relacion con la variable objetivo
Cuando el primer Pokemon supera al segundo en velocidad y estadisticas totales, la probabilidad de first_wins aumenta de forma monotona. Esto explica por que el enfoque de features relacionales fue central en modelado.

### c) Problemas detectados en datos
- Valores faltantes en Type 2 (interpretados como ausencia estructural, no missing aleatorio).
- Duplicados exactos de batallas (~3.9%), con riesgo de inflar metricas si no se controlan.
- Riesgo de sesgo por variables derivadas del resultado historico (WinRate, Wins, n_combats).
- Riesgo de sparsity en combinaciones raras de tipos.

### d) Importancia para modelado
Estos hallazgos definieron decisiones de pipeline:
- Priorizar features diff y ``abs_diff`` porque capturan la ventaja relativa real entre rivales (unidad de desición = batalla).
- Eliminar duplicados antes de entrenar.
- Excluir variables target-derived (`WinRate`, `Wins`, `n_combats`) evita leakage.
- Tratar Type 2 con codificacion estructural explicita.

## 4. Data Preparation

### a) Transformaciones realizadas
- Construccion del dataset a nivel batalla con atributos ``first_`` y ``second_``.
- Feature engineering relacional: diff_* y abs_diff_*.
- Variables de interaccion: same_type1, same_type2, same_generation, both_legendary.
- Pipeline formal con ColumnTransformer para asegurar reproducibilidad.

### b) Manejo de valores faltantes
- Numericas: imputación por mediana.
- Categóricas: imputación por moda.
- Type 2: reemplazo por None como ausencia estructural.

### c) Encoding de categoricas
One-hot encoding con manejo robusto de categorias no vistas (handle_unknown ignore).
Cada categoria se transforma en columnas binarias (0/1), evitando imponer un orden numerico artificial entre categorias.

### d) Feature engineering
Se priorizaron diferencias relativas por combate:
- diff_speed, diff_stats_total, diff_attack, diff_sp_atk, etc.
- Magnitudes absolutas de diferencia para capturar intensidad de ventaja.

### e) Justificacion de decisiones
- Reduce leakage.
- Alinea representacion con la unidad de decision real (batalla).
- Mejora capacidad de generalizacion en relaciones no lineales.

## 5. Modelado

### a) Modelos utilizados
Baselines:
- Dummy Classifier.
- Logistic Regression.
- Decision Tree.

Candidatos de mayor capacidad:
- Random Forest.
- HistGradientBoosting.

### b) Justificacion de eleccion de modelos
- Dummy: piso mínimo de referencia.
- Logistic: baseline lineal interpretable.
- Decision Tree: baseline no lineal simple.
- Random Forest: ensamble robusto con menor varianza.
- HistGradientBoosting: alto rendimiento en tabular y capacidad para no linealidad compleja.
    - Funciona muy bien en ese tipo de datos estructurados.
    - Logra métricas altas (por ejemplo F1, AUC, accuracy) y estables.
    - Generaliza bien fuera de muestra.
    - Suele superar o igualar a baselines en problemas de clasificación/regresión con columnas numéricas y categóricas.
- Nota breve: aqui, "tabular" significa datos en formato tabla (filas = batallas, columnas = variables).

### c) Modelo baseline incluido
Si, se incluyeron tres baselines (Dummy, Logistic y Decision Tree).

## 6. Evaluacion de modelos

### a) Metricas utilizadas
- F1 (metrica principal de seleccion).
- Accuracy.
- Balanced Accuracy.
- ROC-AUC.

### b) Que mide cada metrica
- F1: balance entre precision y recall, útil cuando importa no fallar por exceso de falsos positivos ni falsos negativos.
- Accuracy: proporción total de aciertos.
- Balanced Accuracy: promedio del recall por clase, robusta ante desbalance moderado.
- ROC-AUC: capacidad de separar clases a distintos umbrales.

### c) Comparacion entre modelos (CV-F1)

| Modelo | CV-F1 |
|---|---:|
| HistGradientBoosting tuned | 0.9731 |
| HistGradientBoosting | 0.9683 |
| Random Forest tuned | 0.9679 |
| Decision Tree | 0.9509 |
| Random Forest | 0.9497 |
| Logistic Regression | 0.8803 |
| Dummy | 0.0000 |

Interpretacion:
- Existe ganancia real al pasar de baselines a ensambles.
- El tuning mejora especialmente Random Forest y consolida a HistGradientBoosting como lider.

Resultados finales en test del modelo seleccionado:
- Accuracy: 0.9760
- Balanced Accuracy: 0.9759
- F1: 0.9746
- ROC-AUC: 0.9973

Interpretacion:
Desempeno alto y consistente con CV, sin evidencia fuerte de degradacion fuera de muestra.

## 7. Seleccion del modelo final

### a) Modelo seleccionado
HistGradientBoosting tuned.

### b) Justificacion integral
No se eligio solo por mejor metrica:
- Lidera CV-F1 bajo protocolo homogeno y auditable.
- Mantiene coherencia en metricas complementarias.
- Muestra consistencia CV-test.
- Captura no linealidad detectada en EDA sin introducir complejidad innecesaria de despliegue.

## 8. Interpretabilidad

### a) Variables mas importantes
La evidencia global del proyecto apunta a:
- diff_speed (principal).
- diff_stats_total.
- diff_attack y diff_sp_atk.

### b) Interpretacion del comportamiento del modelo
El modelo favorece escenarios donde el primer Pokemon presenta ventaja relativa clara en velocidad y fuerza total. Esto es coherente con la dinamica competitiva observada en EDA y con la jerarquía de señal estadística reportada.

## 9. Limitaciones del proyecto

### a) Problemas del dataset
- Duplicados de combates.
- Dispersion y baja frecuencia en algunas combinaciones de tipos.
- Dependencia potencial por matchups repetidos.

### b) Riesgos como data leakage
- Variables historicas derivadas del outcome podrian contaminar el entrenamiento si se incluyeran.
- El proyecto lo mitiga excluyendo Winner, WinRate, Wins y n_combats.

### c) Restricciones del enfoque
- Se reportan medias CV, pero no dispersion completa por fold en narrativa principal.
- La interpretabilidad presentada es global, no local por instancia.
- Falta benchmark formal de tiempos de entrenamiento e inferencia.

## 10. Proximos pasos

### a) Mejoras a implementar
- Reportar CV mean +- std e intervalos de confianza.
- Definir umbral operativo en validacion interna y congelarlo antes del test final.
- Incorporar explicabilidad local.

### b) Si hubiera mas tiempo o mas datos
- Robustez por subgrupos y escenarios raros.
- Monitoreo de drift para operacion.
- Evaluacion temporal o por bloques de dependencia mas estrictos.

## 11. Conclusion

### a) Resumen de resultados
Se completo un ciclo metodologico completo y reproducible: comparar, optimizar, seleccionar, validar y documentar.

### b) Que se concluye del modelo
El problema es altamente predecible cuando se representa cada batalla como comparacion entre rivales. La velocidad relativa y la fuerza total relativa concentran la mayor señal util.

### c) Decisiones que permite tomar
- Seleccionar enfrentamientos con mayor probabilidad de victoria.
- Priorizar estrategias donde la ventaja en velocidad y stats totales sea favorable.
- Definir reglas de recomendacion en simulacion competitiva con base cuantitativa.

## Nota para presentacion (criterio de evaluacion)

Para cumplir plenamente el criterio docente:
- No mostrar codigo.
- No mostrar graficos sin interpretacion.
- Explicar siempre que implica cada resultado para la toma de decisiones.
- Defender por que cada decision metodologica reduce riesgo y mejora validez.
