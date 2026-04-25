# Presentacion PowerPoint - Pokemon Model Selection

## Instrucciones de uso
- Documento listo para convertir en diapositivas 1:1.
- No incluye codigo.
- Cada tabla incluye lectura e implicacion para toma de decisiones.
- Duracion sugerida total: 10 a 15 minutos.

---

## Diapositiva 1: Portada
**Titulo:** Pokemon Battle Winner Prediction - Model Selection

**Subtitulo:** Prediccion del ganador de batallas 1v1 con enfoque de modelado tabular

**Equipo:** [Jesus Hernandez]

**Fecha:** 07/04/2026

**Mensaje clave (1 frase):**
Con una representacion relacional por batalla, el problema es altamente predecible y el modelo final alcanza desempeno sobresaliente y estable.

---

## Diapositiva 2: Agenda
1. Contexto del problema
2. Entendimiento del dataset
3. Insights del EDA
4. Data Preparation
5. Modelado
6. Evaluacion de modelos
7. Seleccion del modelo final
8. Interpretabilidad
9. Limitaciones
10. Proximos pasos
11. Conclusiones

---

## Diapositiva 3: Contexto del problema
**Que problema resolvemos:**
Predecir el ganador de una batalla 1v1 entre dos Pokemon, usando atributos del Pokedex y registro historico de combates.

```
El objetivo es predecir el ganador de una batalla Pokémon basándose en los atributos y estadísticas de los combatientes. Este modelo predictivo tiene aplicaciones en estrategia de juego, análisis competitivo y comprensión de mecánicas de combate. El reto principal radica en capturar las complejas interacciones entre tipos, estadísticas y habilidades que determinan el resultado de cada enfrentamiento.
```
**Tipo de problema (clasificacion o regresion):**
Clasificacion binaria.
- Clase 1: gana el primer Pokemon.
- Clase 0: gana el segundo Pokemon.

**Caso de uso real / relevancia:**
En un simulador competitivo, permite anticipar ventaja antes del combate, recomendar enfrentamientos favorables y apoyar decisiones tacticas.

**Mensaje clave:**
El valor del proyecto no es solo predecir, sino apoyar decisiones de estrategia con evidencia cuantitativa.

---

## Diapositiva 4: Entendimiento del dataset
**Origen de datos:**
- pokemon.csv (atributos por Pokemon)
- combats.csv (batallas y ganador observado)

**Que representa cada fila:**
- pokemon.csv: 1 Pokemon por fila
- combats.csv: 1 batalla por fila

**Tamano del dataset:**
- pokemon.csv: 799 registros utiles
- combats.csv: 49,999 batallas utiles

**Mensaje clave:**
La unidad analitica final es la batalla, por eso el dataset debe transformarse de entidad Pokemon a comparacion entre rivales.

---

## Diapositiva 5: Variables del dataset
| Grupo | Variables | Rol |
|---|---|---|
| Numericas | HP, Attack, Defense, Sp. Atk, Sp. Def, Speed | Base para construir ventajas relativas |
| Categoricas | Type 1, Type 2, Generation | Contexto estructural de matchup |
| Binarias | Legendary, is_mega, variables de coincidencia | señal contextual complementaria |
| Objetivo | first_wins | Variable a predecir |
| Excluidas por leakage | Winner, WinRate, Wins, n_combats | Prohibidas para entrenamiento |

**Interpretacion (2-3 lineas):**
La estructura del problema exige priorizar variables relacionales (diferencias entre rivales) y excluir variables derivadas del resultado historico. Esta decision protege validez y evita sobreestimar el rendimiento.

---

## Diapositiva 6: Principales insights del EDA (hallazgos)
**Hallazgo 1:** La señal principal es relacional, no individual.
- Evidencia: diff_speed (corr 0.68, AUC univariado orientado 0.93).
- Implicacion para modelado: priorizar diff_* como nucleo del set de features.

**Hallazgo 2:** La fuerza total relativa tambien aporta señal fuerte.
- Evidencia: diff_stats_total (corr 0.47, AUC 0.77).
- Implicacion para modelado: retener stat-based relational features como bloque principal.

**Hallazgo 3:** Variables grupales son secundarias y parcialmente confusas.
- Evidencia: efectos de Legendary/Mega/Type se reducen al controlar por stats.
- Implicacion para modelado: tratarlas como apoyo, no como explicacion primaria.

---

## Diapositiva 7: EDA y calidad de datos
**Problemas detectados:**
- Missing values: Type 2 con ausencia estructural (no missing aleatorio).
- Duplicados: ~3.9% de batallas exactas.
- Outliers / sesgos: posible dominancia de Speed y combinaciones raras de tipos (sparsity).
- Riesgos de leakage: Winner, WinRate, Wins, n_combats.

**Por que es importante para modelar:**
Estos riesgos pueden inflar metricas y deteriorar generalizacion. El EDA definio reglas explicitas de preparacion para mantener validez metodologica.

---

## Diapositiva 8: Data Preparation
**Transformaciones principales:**
- Construccion del dataset a nivel batalla (first_/second_).
- Deduccion de features relacionales (diff_* y abs_diff_*).
- Pipeline con ColumnTransformer para trazabilidad y reproducibilidad.

**Manejo de faltantes:**
- Numericas: imputacion por mediana.
- Categoricas: imputacion por moda.
- Type 2: reemplazo por None (ausencia estructural).

**Encoding de categoricas:**
One-hot encoding con handle_unknown=ignore para robustez ante categorias no vistas.

**Feature engineering realizado:**
- diff_speed, diff_stats_total, diff_attack, diff_sp_atk, etc.
- Features de interaccion: same_type1, same_type2, same_generation, both_legendary.

**Justificacion de decisiones:**
Evitan leakage, respetan la unidad de decision real (batalla) y mejoran capacidad de generalizacion.

---

## Diapositiva 9: Modelado
**Modelos evaluados (minimo 3):**
- Baseline 1: Dummy Classifier
- Baseline 2: Logistic Regression
- Baseline 3: Decision Tree
- Modelo 4: Random Forest
- Modelo 5: HistGradientBoosting

**Por que se eligieron:**
Se cubrio un espectro de complejidad: desde referencia minima (Dummy), modelos interpretables (Logistic), no lineales simples (Tree) y ensambles robustos para datos tabulares (RF, HGB).

---

## Diapositiva 10: Metricas de evaluacion
**Metricas usadas:**
- F1
- Accuracy
- Balanced Accuracy
- ROC-AUC

**Que mide cada metrica (en lenguaje simple):**
- F1: equilibrio entre precision y recall.
- Accuracy: porcentaje total de aciertos.
- Balanced Accuracy: promedio del recall por clase.
- ROC-AUC: capacidad de separar clases en distintos umbrales.

---

## Diapositiva 11: Comparacion de modelos
| Modelo | CV-F1 | Accuracy | Balanced Accuracy | ROC-AUC | Comentario |
|---|---:|---:|---:|---:|---|
| Dummy | 0.000 | - | - | - | Referencia minima, sin capacidad predictiva util |
| Logistic Regression | 0.953 | - | - | - | Baseline lineal fuerte y estable |
| Decision Tree | 0.959 | - | - | - | Mejor baseline; capta no linealidad moderada |
| Random Forest tuned | 0.971 | - | - | - | Tuning con mejora marcada (+0.014 CV-F1) |
| HistGradientBoosting tuned (final) | 0.975 | 0.979 (test) | 0.979 (test) | 0.998 (test) | Mejor equilibrio global y consistencia CV-test |

**Interpretacion de la comparacion:**
La mejora de baselines a ensambles es clara. El mejor CV-F1 lo obtiene HistGradientBoosting tuned y ademas confirma rendimiento alto en test.
La actualizacion final de Optuna elevo el rendimiento sin romper la coherencia metodologica entre CV y test.

---

## Diapositiva 12: Seleccion del modelo final
**Modelo seleccionado:** HistGradientBoosting tuned.

**Criterios de seleccion (no solo mejor metrica):**
- Rendimiento: lider en CV-F1.
- Robustez / generalizacion: consistencia entre CV y test.
- Complejidad y costo computacional: alta capacidad sin sobrecomplicar despliegue.
- Alineacion con el problema: captura no linealidad en datos tabulares con features relacionales.

**Mensaje clave:**
Se selecciono por equilibrio metodologico y operativo, no solo por ganar en un numero.

---

## Diapositiva 13: Interpretabilidad
**Variables mas importantes:**
1. diff_speed
2. diff_stats_total
3. diff_attack
4. diff_sp_atk

**Como se interpreta el comportamiento del modelo:**
Cuando el primer Pokemon tiene ventaja relativa en velocidad y stats totales, su probabilidad de victoria crece de forma consistente.

**Decision practica que habilita:**
Recomendar enfrentamientos donde exista ventaja relativa clara en velocidad y fuerza total.

---

## Diapositiva 14: Limitaciones
**Limitaciones del dataset:**
- Duplicados de combates y matchups repetidos.
- Baja frecuencia en combinaciones raras de tipos (sparsity).

**Riesgos metodologicos (incluye leakage):**
- Inclusion accidental de variables target-derived.
- Dependencia entre observaciones si el split no controla pares repetidos.

**Restricciones del enfoque:**
- La narrativa principal reporta medias CV, sin dispersion completa por fold.
- Interpretabilidad mayormente global, no local por instancia.

---

## Diapositiva 15: Proximos pasos
**Mejoras inmediatas:**
1. Reportar CV mean +- std e intervalos de confianza.
2. Definir y congelar umbral operativo antes de test final.
3. Incorporar explicabilidad local por prediccion.

**Que hariamos con mas tiempo o mas datos:**
1. Robustez por subgrupos y escenarios raros.
2. Monitoreo de drift en operacion.
3. Evaluacion temporal o por bloques de dependencia mas estrictos.

---

## Diapositiva 16: Conclusion
**Resumen de resultados (3 bullets):**
- El problema es altamente predecible con representacion relacional por batalla.
- Las señales dominantes son diff_speed y diff_stats_total.
- HistGradientBoosting tuned logra el mejor equilibrio de rendimiento y robustez.

**Que se puede concluir del modelo:**
El modelo captura patrones competitivos consistentes y generaliza bien fuera de muestra.

**Que decisiones permite tomar:**
Seleccion de enfrentamientos favorables, priorizacion tactica y recomendaciones de estrategia con base cuantitativa.

---

## Diapositiva 17: Cierre y preguntas
**Gracias**

**Contacto:** [Completar]

**Q&A**

---

## Notas de apoyo visual (Diapositivas 6-17)

Usa este bloque como guia para agregar imagenes/tablas sin perder trazabilidad de origen.

| Diapositiva | Visual recomendado | De donde se obtiene | Nota de uso en exposicion |
|---|---|---|---|
| 6. Insights del EDA | Heatmap de correlaciones relacionales | reports/figures/stats_vs_win_probability_correlation.png | Resaltar que diff_speed y diff_stats_total concentran la señal. |
| 6. Insights del EDA | Tabla corta de top señales (corr + AUC) | reports/feature_signal_summary.csv | Mostrar solo top 5 para no saturar; cerrar con implicacion para modelado. |
| 7. EDA y calidad de datos | Vista distribucional general del dataset | reports/figures/pokemon_distributions_overview.png | Conectar visualmente calidad/cobertura con decisiones de limpieza. |
| 7. EDA y calidad de datos | Evidencia de duplicados y sensibilidad | reports/robustness_threshold_sensitivity.csv | Usar como mini-tabla para explicar por que se deduplica y se controla dependencia. |
| 8. Data Preparation | Diagrama de flujo del pipeline de preparacion (hecho en slides) | Fuente de contenido: notebooks/Data Preparation.ipynb y reports/guia_data_preparation_pokemon.md | Mostrar pasos: dedup -> feature engineering -> split por grupos -> preprocess pipeline. |
| 9. Modelado | Grafico de familias de modelos (baseline vs candidatos) | Fuente de contenido: notebooks/Modeling and Model Selection.ipynb | Puede ser visual manual (bloques) para enfatizar criterio de complejidad incremental. |
| 10. Metricas de evaluacion | Tarjetas de metricas con definicion corta | Fuente de contenido: reports/informe_presentacion_modeling.md | Evitar grafico decorativo: priorizar lectura practica de cada metrica. |
| 11. Comparacion de modelos | Tabla comparativa actual (ya incluida) | reports/pokemon_model_selection_results.csv + reports/pokemon_test_metrics.json | Mantener nota metodologica: CV para ranking multi-modelo y test para modelo final. |
| 11. Comparacion de modelos | Barra horizontal de CV-F1 por modelo | reports/pokemon_model_selection_results.csv | Orden descendente para visualizar brecha entre baseline y ensambles tuneados. |
| 12. Seleccion final | Matriz de decision (rendimiento, robustez, costo, alineacion) | Fuente de contenido: reports/informe_presentacion_modeling.md | Visual tipo semaforo para justificar decision mas alla de un solo numero. |
| 13. Interpretabilidad | Tabla de variables mas importantes (ya listadas) | reports/feature_signal_summary.csv | Aclarar que es evidencia de señal global en entrenamiento (alineada con EDA). |
| 13. Interpretabilidad | Curvas por deciles (relacion stats-ganar) | reports/figures/stats_vs_win_probability_deciles.png | Mostrar monotonia de la señal y traducir a regla tactica interpretable. |
| 14. Limitaciones | Heatmap de enfrentamientos por tipo (sparsity y heterogeneidad) | reports/figures/type1_matchup_heatmap_corrected.png | Usar para justificar riesgo de combinaciones raras y generalizacion por subgrupos. |
| 14. Limitaciones | Top10 de winrate por tipo con cautela muestral | reports/figures/type1_top10_winrate_corrected.png | Aclarar que es descriptivo y no causal; evitar sobreinterpretacion. |
| 15. Proximos pasos | Roadmap visual de 3 bloques (robustez, umbral, explicabilidad local) | Fuente de contenido: reports/informe_presentacion_modeling.md | Timeline simple con prioridad inmediata vs mediano plazo. |
| 16. Conclusion | Slide de KPIs finales (cards) | reports/pokemon_test_metrics.json + reports/pokemon_model_selection_results.csv | Incluir 3 mensajes de negocio ligados a F1/ROC-AUC/consistencia CV-test. |
| 17. Cierre y preguntas | Slide limpia con QR o enlace al repo/reportes | README.md + reports/informe_presentacion_modeling.md | Facilita preguntas tecnicas y trazabilidad post-presentacion. |

### Nota de trazabilidad rapida

- Figuras EDA: reports/figures/*.png
- Ranking de modelos: reports/pokemon_model_selection_results.csv
- Metricas finales test: reports/pokemon_test_metrics.json
- Narrativa tecnica: reports/informe_presentacion_modeling.md
- Soporte de preparacion: reports/guia_data_preparation_pokemon.md
