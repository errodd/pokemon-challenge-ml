---
alias:
tags:
creado: 16/02/2026
modificado: 16/02/2026
tipo: Concepto
base:
---
# EDA Batallas Pokémon
>Python 3.13.2
>Librerías: mathprolib, numpy, pandas

## Comandos python
**Crear entorno virtual** Python3 -m venv ``<nombre>``
**Entrar entorno virtual** source ``<nombre del entorno>/bin/activate``
**instalar dependencias** pip install -r requirements.txt
**Apagar** deactivate
**Encender** activate
**Limpiar terminal** clear

### Nota de evaluación EDA
Puntos positivos

- El notebook ejecuta sin errores críticos.
- Se realizó una exploración inicial del dataset.
- Se analizaron valores faltantes.
- Se utilizaron visualizaciones acordes al tipo de variables.
- Existe intención de relacionar variables con el objetivo del análisis.

---

**Observación crítica 1: Falta de estructura formal**

El notebook no sigue claramente la estructura esperada para el proyecto:

1. Configuración
2. Carga de datos
3. Limpieza
4. EDA
5. Feature engineering
6. Conclusiones orientadas al modelado

Las secciones no están delimitadas explícitamente ni acompañadas de una narrativa técnica sólida en Markdown. El flujo es mayormente exploratorio y no estratégico.

En un proyecto de Machine Learning completo, la organización es parte de la calidad técnica.

---

**Observación crítica 2: Análisis mayormente descriptivo (Punto clave)**

El análisis realizado se mantiene en un nivel descriptivo:

- Se muestran distribuciones.
- Se presentan gráficos.
- Se calculan estadísticas básicas.

Sin embargo, falta profundidad en:

- Identificación de variables relevantes.
- Detección de posibles problemas estructurales.
- Análisis de colinealidad.
- Análisis de cardinalidad en variables categóricas.
- Cuantificación rigurosa de missing values.
- Evaluación explícita del impacto de decisiones de limpieza.

El EDA debe reducir incertidumbre y producir decisiones concretas para el modelado posterior.

Actualmente no se observan decisiones técnicas claras derivadas del análisis.

---

**Observación adicional: Análisis de bajo impacto**

Se incluyen gráficos o tablas que:

- Repiten información evidente.
- No derivan en decisiones.
- No se conectan con el modelado futuro.

Regla importante:

Si un análisis no termina en una acción concreta sobre una variable (transformar, eliminar, codificar, imputar, etc.), su valor estratégico es limitado.

---

**Mejoras obligatorias para la siguiente entrega**

A. Estructura formal del notebook

- Delimitar claramente las secciones.
- Incluir bloque de configuración inicial.
- Incorporar Markdown técnico explicativo.
- Cerrar con conclusiones estratégicas.

B. Profundidad analítica

- Clasificar variables por tipo.
- Cuantificar porcentaje exacto de missing values.
- Identificar variables con alta cardinalidad.
- Detectar posibles variables redundantes.
- Evaluar correlaciones relevantes con el target.

C. Orientación al modelado

El EDA debe responder explícitamente:

- ¿Qué variable se quiere predecir?
- ¿Qué variables parecen predictivas?
- ¿Qué problemas técnicos existen?
- ¿Qué transformaciones serán necesarias?

Actualmente el análisis no está claramente conectado con la siguiente etapa del proyecto.

---

**Impacto en el proyecto final**

Este trabajo es la base del modelo final.

Si el EDA no identifica correctamente:

- Variables problemáticas,
- Variables redundantes,
- Posibles sesgos,
- Necesidad de transformaciones,

El modelo posterior será débil o mal especificado.

Un EDA superficial produce modelos superficiales.

---

El trabajo cumple con lo mínimo esperado, pero necesita mayor profundidad técnica y orientación estratégica.

Se espera que en la próxima entrega:

1. Se estructure formalmente el notebook.
2. Se documenten decisiones técnicas explícitas.
3. Se conecte cada análisis con el modelado futuro.
4. Se eleve el nivel de pensamiento crítico.

El objetivo del curso no es solo explorar datos, sino formar criterio profesional en Ciencia de Datos.