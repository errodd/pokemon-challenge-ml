# pokemon-challenge-ml

Proyecto de Machine Learning para predecir el ganador de una batalla 1v1 de Pokemon a partir de datos tabulares.

## 1) Que resuelve este proyecto

Dado un par de Pokemon en combate (First_pokemon y Second_pokemon), el sistema predice si gana el primero.

- Unidad de modelado: una batalla.
- Target de entrenamiento: first_wins (binario).
- Tipo de problema: clasificacion binaria.

## 2) Estado actual

El flujo principal ya esta implementado de extremo a extremo:

1. EDA completado.
2. Data Preparation completado.
3. Modeling and Model Selection completado.
4. Artefactos finales y reportes generados.

Metricas finales en test del modelo seleccionado (segun reports/pokemon_test_metrics.json):

- Accuracy: 0.979
- Balanced Accuracy: 0.979
- F1: 0.978
- ROC-AUC: 0.998

## 3) Guia rapida de navegacion

Si es tu primera vez en el repo, sigue este orden:

1. notebooks/EDA.ipynb
2. notebooks/Data Preparation.ipynb
3. notebooks/Modeling and Model Selection.ipynb
4. reports/informe_presentacion_modeling.md
5. reports/presentacion_powerpoint_modeling_completa.md

## 4) Estructura del repositorio

- data/
	- pokemon.csv: atributos por Pokemon.
	- combats.csv: historial de batallas y ganador.

- notebooks/
	- EDA.ipynb: analisis exploratorio y riesgos metodologicos.
	- Data Preparation.ipynb: limpieza, features, split y pipeline.
	- Modeling and Model Selection.ipynb: comparativa de modelos, tuning y evaluacion final.

- src/
	- predict.py: modulo de inferencia (ingenieria de features + prediccion).

- artifacts/
	- preprocess_pipeline_pokemon.joblib: pipeline de transformacion.
	- split_data_pokemon.joblib: particiones train/test persistidas.
	- feature_manifest_pokemon.json: contrato de features y decisiones.
	- final_model_pipeline_pokemon.joblib: modelo final entrenado.
	- model_card_pokemon.json: metadatos de seleccion y metricas.

- app.py: aplicacion web Gradio para prediccion interactiva.
- requirements-app.txt: dependencias de la aplicacion de despliegue.
- Dockerfile: imagen Docker lista para produccion.

- reports/
	- EDA_transcripcion_es.md: narracion del EDA.
	- guia_data_preparation_pokemon.md: guia detallada de preparacion.
	- informe_presentacion_modeling.md: informe final para presentacion.
	- pokemon_model_selection_results.csv: ranking final por CV-F1.
	- pokemon_test_metrics.json: metricas de test del modelo final.
	- presentacion_powerpoint_modeling_completa.md: version lista para slides.
	- plantilla_presentacion_powerpoint.md: plantilla editable.
	- figures/: imagenes exportadas.

## 5) Como ejecutar localmente

Requisitos:

- Python 3.12 recomendado.
- Entorno virtual.

Pasos:

1. Crear y activar entorno virtual.
2. Instalar dependencias.
3. Abrir notebooks en orden de flujo.

Comandos sugeridos:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Luego:
- Opcion A: abrir el proyecto en VS Code y ejecutar los notebooks desde el editor.
- Opcion B: iniciar interfaz clasica de notebooks desde terminal con jupyter notebook.

## 6) Flujo metodologico (resumen)

1. EDA:
- audita calidad de datos,
- detecta leakage potencial,
- confirma que las senales mas fuertes son relacionales (diff_speed, diff_stats_total).

2. Data Preparation:
- deduplica batallas,
- crea features relacionales,
- aplica split por grupos (matchup_key) para evitar dependencia train-test,
- persiste pipeline y manifiesto.

3. Modeling:
- compara baselines y candidatos,
- optimiza hiperparametros con Optuna,
- selecciona modelo final por CV-F1,
- evalua una sola vez en test hold-out,
- guarda modelo final y model card.

## 7) Donde ver cada resultado clave

- Ranking final de modelos: reports/pokemon_model_selection_results.csv
- Metricas finales de test: reports/pokemon_test_metrics.json
- Modelo final serializado: artifacts/final_model_pipeline_pokemon.joblib
- Contrato tecnico del modelo: artifacts/model_card_pokemon.json

## 8) Convenciones importantes del proyecto

- No usar variables con leakage (Winner, WinRate, Wins, n_combats) como features de entrenamiento.
- Mantener el test hold-out aislado hasta la evaluacion final.
- Conservar reproducibilidad con RANDOM_STATE fijo y artefactos persistidos.

## 9) Siguiente trabajo recomendado

- Analisis de robustez por subgrupos.
- Reporte de dispersion por fold (mean +- std).
- Explicabilidad local por instancia para casos criticos.
- Monitoreo de drift si se pasa a entorno productivo.

## 10) Despliegue de la aplicacion web

El modelo esta listo para ser usado a traves de una interfaz web construida con [Gradio](https://gradio.app).

### Archivos clave del despliegue

- `app.py`: aplicacion Gradio (interfaz de usuario).
- `src/predict.py`: logica de ingenieria de features e inferencia.
- `requirements-app.txt`: dependencias minimas para ejecutar la app.
- `Dockerfile`: imagen Docker lista para produccion.

### Opcion A: ejecucion local

```bash
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements-app.txt
python app.py
```

Abre el navegador en `http://localhost:7860`.

### Opcion B: Docker

```bash
docker build -t pokemon-predictor .
docker run -p 7860:7860 pokemon-predictor
```

Abre el navegador en `http://localhost:7860`.

### Opcion C: Hugging Face Spaces (despliegue publico gratuito)

1. Crea un nuevo Space en [huggingface.co/spaces](https://huggingface.co/spaces) eligiendo SDK **Gradio**.
2. Sube `app.py`, `src/`, `artifacts/`, `data/pokemon.csv` y `requirements-app.txt`.
3. Hugging Face construye e inicia la app automaticamente.

### Uso de la interfaz

1. Selecciona el primer Pokemon en el desplegable izquierdo.
2. Selecciona el segundo Pokemon en el desplegable derecho.
3. Pulsa **Predict Battle**.
4. La app muestra el ganador predicho, el nivel de confianza y una tabla comparativa de estadisticas.