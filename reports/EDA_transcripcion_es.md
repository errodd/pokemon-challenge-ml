# Transcripción narrativa del EDA de batallas Pokemon

## Propósito general

Este documento resume y transcribe el contenido analítico del notebook EDA.ipynb sin incluir código. Su objetivo es explicar, en español y de forma ordenada, qué preguntas intenta responder el análisis exploratorio, qué decisiones metodológicas propone, qué supuestos adopta y cuáles son sus conclusiones principales de cara a un problema de modelado supervisado.

El EDA está planteado para una tarea de clasificación binaria a nivel de batalla. La unidad de análisis no es cada Pokemon de forma aislada, sino cada enfrentamiento entre dos Pokemon. El objetivo operativo es predecir si gana el primer Pokemon de la batalla, variable que el notebook denomina first_wins.

La lógica del análisis sigue tres preguntas rectoras:

1. Si los datos son estructuralmente utilizables para aprendizaje supervisado.
2. Qué señales parecen realmente relevantes para la predicción.
3. Qué hallazgos deben considerarse solo descriptivos y no deben convertirse en variables de entrenamiento.

La idea central del notebook es que el EDA debe estar subordinado al modelado. Por eso no se limita a describir distribuciones, sino que intenta separar evidencia útil para diseñar el pipeline de evidencia meramente contextual.

## 1. Preparación y carga de datos

El notebook comienza estableciendo el entorno de trabajo, las rutas de datos y las rutas de salida para figuras y reportes. Después carga dos tablas:

- Una tabla a nivel de Pokemon, con atributos de cada criatura del Pokedex.
- Una tabla a nivel de combate, con el registro de enfrentamientos y el ganador.

### Qué aporta esta sección

Esta parte no genera conclusiones analíticas profundas, pero deja claro que el proyecto combina dos granularidades distintas:

- variables intrínsecas del Pokemon,
- resultados observados de las batallas.

Ese punto es importante porque el modelado final debe transformar la información del Pokemon individual en variables comparativas entre los dos oponentes de cada batalla.

### Presunción implícita

Se asume que ambas fuentes son compatibles y pueden vincularse mediante los identificadores de Pokemon sin problemas de resolución de entidades.

## 2. Hoja de ruta analítica

El notebook explicita su estructura antes de entrar en el análisis. Propone este recorrido:

1. auditoría de datos y riesgos estructurales,
2. decisiones preliminares de modelado,
3. análisis de la variable objetivo,
4. evidencia principal basada en diferencias de estadísticas,
5. análisis secundarios por grupos,
6. síntesis final sobre relevancia de variables y riesgos de validez.

### Qué aporta esta sección

La utilidad de esta hoja de ruta es metodológica. Evita mezclar bloques descriptivos con bloques realmente importantes para la predicción y deja claro que no todas las secciones tienen el mismo peso inferencial.

## 3. Auditoría de datos

La auditoría separa las variables según su rol para el modelado, no solo según su tipo de dato. El notebook distingue tres familias:

- atributos cuantitativos relevantes para combate, como HP, Attack, Defense, Sp. Atk, Sp. Def y Speed,
- atributos estructurales de baja cardinalidad, como Generation, Legendary, Type 1 y Type 2,
- identificadores de alta cardinalidad, como el número de Pokemon, el nombre y los IDs usados en las batallas.

### Qué se analiza aquí

En esta sección se inspeccionan:

- tipos de variables,
- presencia de valores faltantes,
- duplicados,
- cardinalidad,
- cobertura entre los IDs del registro de combates y los del Pokedex.

### Hallazgos principales

- La variable Type 2 es la única con nulos relevantes.
- Esos nulos no se interpretan como una falta aleatoria de datos, sino como ausencia estructural de un segundo tipo.
- Los identificadores tienen cardinalidad alta y no deben entrar como predictores brutos.
- La cobertura entre los IDs de combates y los del Pokedex es completa, por lo que no aparece un problema de integración entre tablas.
- Hay batallas duplicadas exactas, y su proporción es de aproximadamente 3.9 por ciento.

### Presunciones y decisiones derivadas

De esta auditoría salen varios supuestos operativos:

- Type 2 debe codificarse como ausencia explícita y no como missing aleatorio.
- Los identificadores solo sirven para enlazar tablas o derivar atributos, no como variables del modelo.
- Las batallas duplicadas pueden inflar el desempeño aparente y deben eliminarse o controlarse en validación.

## 4. Riesgos estructurales para modelado

Tras la auditoría, el notebook sintetiza tres riesgos que considera críticos antes de cualquier análisis guiado por el objetivo:

- dependencia artificial por batallas duplicadas,
- fuga de información si se usan identificadores o métricas derivadas del resultado,
- interpretación errónea de los nulos de Type 2.

### Qué aporta esta sección

Esta parte convierte observaciones exploratorias en restricciones de diseño del pipeline. El EDA deja de ser solo descripción y empieza a fijar reglas de preprocesamiento.

## 5. Decisiones preliminares de modelado

Antes de estudiar la variable objetivo, el notebook adelanta un conjunto de decisiones que considera ya justificadas:

- eliminar duplicados exactos,
- representar Type 2 como ausencia estructural,
- excluir identificadores crudos,
- construir variables a nivel de batalla,
- separar métricas descriptivas históricas de predictores aptos para entrenamiento.

### Interpretación

Esto muestra una postura metodológica clara: no todo lo medible es una buena variable. El notebook intenta distinguir entre variables informativas y variables contaminadas por fuga de información.

## 6. Análisis de la variable objetivo

El notebook define la tarea supervisada de la siguiente forma:

- first_wins = 1 si el ganador coincide con el primer Pokemon de la fila,
- first_wins = 0 en caso contrario.

### Qué se analiza aquí

Se estudian tres aspectos:

- balance de clases,
- línea base ingenua,
- relación entre la definición del objetivo y la estructura duplicada de los datos.

### Resultados principales

- La clase second_wins representa aproximadamente 52.8 por ciento de los casos.
- La clase first_wins representa aproximadamente 47.2 por ciento.
- La baseline ingenua por mayoría de clase queda en 52.8 por ciento.
- El desbalance es leve, no extremo.

### Conclusiones del bloque

- No hay una justificación inmediata para aplicar técnicas agresivas de rebalanceo.
- La accuracy sola no es suficiente como métrica, porque la distribución no es totalmente simétrica.
- La estrategia de validación debe ser cuidadosa debido a duplicados y repeticiones de enfrentamientos.

### Presunción clave

Se asume que el orden de los Pokemon en la tabla puede modelarse de forma consistente mediante variables relativas. Eso permite trabajar con un target orientado al primer Pokemon sin convertir el problema en uno dependiente del orden arbitrario de la fila.

## 7. Contexto descriptivo histórico

El notebook construye métricas históricas como:

- número de combates por Pokemon,
- número de victorias,
- porcentaje histórico de victorias o WinRate.

### Qué se busca con este bloque

No se busca justificar variables de entrenamiento, sino describir el historial observado de competencia de cada Pokemon y detectar perfiles aparentemente dominantes.

### Resultados destacados

- El promedio de apariciones por Pokemon es de 125 combates.
- El WinRate medio es de 49.09 por ciento.
- Algunos Pokemon, en especial varias formas Mega, aparecen con tasas históricas de victoria muy altas.

### Lectura correcta según el propio notebook

El análisis insiste en que estas métricas deben interpretarse con cautela:

- un WinRate alto debe leerse junto con el número de combates,
- una tasa histórica alta no prueba un efecto causal propio,
- estas métricas derivan del resultado observado y por tanto introducirían fuga de información si se usan como predictores directos.

### Conclusión del bloque

El valor de este apartado es descriptivo. Sirve para contextualizar el universo competitivo, pero no debe contaminar el modelo final.

## 8. Contexto descriptivo estructural

Luego se presenta un bloque visual de contexto general sobre:

- frecuencia de tipos,
- distribución por generación,
- frecuencia de Pokemon legendarios y formas Mega,
- valores medios, mínimos y máximos de estadísticas base.

### Qué aporta esta sección

Este bloque ayuda a entender la composición del dataset y sus desbalances naturales. También permite anticipar qué grupos pueden estar sobre o subrepresentados.

### Presunción metodológica

Se entiende como evidencia secundaria. El notebook deja claro que estas distribuciones no bastan para priorizar variables predictoras, porque no están conectadas todavía de forma directa con el resultado de la batalla.

## 9. Evidencia principal: diferencias relativas de estadísticas y probabilidad de victoria

Este es el núcleo analítico del EDA. El notebook transforma las estadísticas individuales en variables relativas por batalla, comparando al primer Pokemon con el segundo.

### Qué se analiza

Para cada combate se calculan diferencias en:

- HP,
- Attack,
- Defense,
- Sp. Atk,
- Sp. Def,
- Speed,
- Stats_Total.

Después se estudia cuánto se asocia cada diferencia con la probabilidad de victoria del primer Pokemon.

### Resultados principales

El patrón encontrado es muy claro:

- Speed es la señal más fuerte con diferencia, con una correlación aproximada de 0.678 respecto a first_wins.
- Stats_Total es la segunda familia de variables más importante, con correlación cercana a 0.470.
- Attack y Sp. Atk aparecen después, con correlaciones en torno a 0.362 y 0.349.
- Sp. Def y HP muestran señales intermedias.
- Defense es la estadística menos influyente dentro de este bloque, con correlación cercana a 0.079.

El notebook también compara la tasa de victoria del primer Pokemon cuando su estadística es mayor, igual o menor que la del rival. Esa comparación confirma que las ventajas relativas grandes se asocian con aumentos importantes en la probabilidad de ganar.

### Interpretación de fondo

La conclusión central es que las diferencias relativas entre oponentes explican mejor el resultado que cualquier atributo descriptivo agregado. En particular:

- la velocidad relativa domina el resto de señales,
- el total agregado de estadísticas añade una segunda capa fuerte de capacidad predictiva,
- la ofensiva parece importar más que la defensa,
- las curvas por deciles muestran una relación monotónica, no una relación causal demostrada.

### Supuestos y cautelas

El notebook introduce una advertencia importante: la fuerza extrema de Speed es útil para modelar, pero también lo bastante grande como para exigir escepticismo. Puede haber reglas implícitas del dataset o sesgos de construcción que amplifiquen su papel.

### Conclusión del bloque

Este apartado establece la jerarquía principal de variables:

1. diff_speed,
2. diff_total,
3. diferencias ofensivas como diff_attack y diff_sp_atk,
4. señales secundarias como defensa, generación o grupos.

## 10. Mapas de calor complementarios

El notebook añade dos heatmaps:

- uno entre estadísticas base y WinRate histórico,
- otro entre diferencias de estadísticas y first_wins.

### Qué función cumplen

No reemplazan al bloque principal, sino que lo complementan.

- El heatmap con WinRate es descriptivo y está contaminado por ser target-derived.
- El heatmap de diff_* es más alineado con la tarea predictiva real.

### Conclusión

Ambos mapas refuerzan la idea de que las diferencias relativas son más útiles para modelado que los agregados históricos.

## 11. Análisis secundario por grupos: legendarios, Mega, generación y tipos

El notebook declara explícitamente que estas secciones son secundarias respecto al bloque de diferencias de estadísticas. Su función no es competir con la explicación principal, sino evaluar si ciertos grupos añaden señal adicional o si solo reflejan diferencias de atributos base.

## 12. Análisis de Legendary y Mega

Este bloque compara grupos de Pokemon según si son legendarios, Mega o ambos. Lo hace en varios niveles:

- resumen histórico por grupo,
- combates directos con duplicados removidos,
- intervalos de confianza de Wilson,
- subsamples controlados donde diff_speed y diff_total son pequeños,
- matrices de enfrentamiento entre grupos.

### Resultados principales

- En combates directos deduplicados, los legendarios vencen a los no legendarios aproximadamente en 80.58 por ciento de los casos analizados.
- Las formas Mega vencen a las no Mega aproximadamente en 73.35 por ciento.
- A nivel descriptivo agregado, los grupos con mayor Stats_Total y mayor Speed también concentran mayor WinRate histórico.

### Qué intenta demostrar realmente el bloque

No intenta probar que ser legendario o Mega cause la victoria por sí mismo. Intenta verificar si el efecto bruto persiste cuando se compara a estos grupos de forma más cuidadosa.

### Resultado más importante del control parcial

Cuando el análisis se restringe a combates con diferencias pequeñas en velocidad y estadísticas totales:

- la ventaja de Legendary cae a 36.0 por ciento en una muestra de 25 casos,
- la ventaja de Mega cae a 48.78 por ciento en una muestra de 41 casos.

### Interpretación correcta

La caída es tan fuerte que el notebook concluye que gran parte de la ventaja observada en esos grupos está mediada por atributos base, sobre todo velocidad y fuerza total, más que por una condición de grupo autónoma.

### Supuestos y límites

- La variable is_mega se deriva del nombre, así que es una aproximación práctica, no una etiqueta perfectamente curada.
- Los subsamples controlados son pequeños, así que no permiten afirmaciones fuertes por sí solos.

### Conclusión del bloque

Legendary e is_mega pueden conservarse como variables auxiliares, pero no deben interpretarse como explicación primaria del resultado.

## 13. Análisis de generación

La generación se estudia como una señal contextual secundaria. El notebook revisa:

- si pertenecer a una generación más alta se asocia con mayor probabilidad de victoria,
- la matriz de enfrentamientos entre generaciones,
- un control parcial ajustando por Speed y Stats_Total.

### Resultados principales

- Cuando el primer Pokemon pertenece a una generación superior, gana alrededor de 48.14 por ciento de las veces.
- Cuando ambos son de la misma generación, la tasa observada es cercana a 47.56 por ciento.
- Cuando el primero pertenece a una generación inferior, gana alrededor de 46.09 por ciento.

La diferencia existe, pero es pequeña.

### Resultado bajo control parcial

Al restringir el análisis a combates más balanceados en velocidad y fuerza total, la ventaja de la generación superior queda en 49.59 por ciento sobre 972 casos, es decir, prácticamente neutral.

### Conclusión del bloque

La generación muestra una señal descriptiva débil. La mayor parte de su aparente efecto parece estar mediada por las estadísticas base. Por tanto, Generation puede mantenerse como variable contextual de baja prioridad, pero no como eje explicativo principal.

## 14. Análisis de tipos

El bloque de tipos separa claramente este análisis del de generación y estudia:

- matrices de enfrentamiento entre Type 1 frecuentes,
- tasas de victoria dirigidas por Type 1,
- perfiles combinados Type 1 / Type 2,
- comparación entre Pokemon de un solo tipo y Pokemon de doble tipo,
- control parcial por velocidad y estadísticas totales.

### Qué revela este análisis

Los tipos sí generan estructura descriptiva interesante. Algunas categorías de Type 1 muestran tasas dirigidas claramente por encima o por debajo del 50 por ciento, y el heatmap de enfrentamientos entre tipos frecuentes exhibe contrastes muy marcados.

En la visualización resumida aparecen entre los tipos con mayor tasa dirigida Dragon y Electric, mientras que otros como Rock o Bug quedan más abajo. Sin embargo, el notebook insiste en que estas diferencias deben leerse junto con el tamaño muestral de cada celda.

### Resultado sobre mono-tipo vs doble tipo

- En bruto, los Pokemon con segundo tipo parecen tener ventaja, con una tasa de victoria de 56.68 por ciento en 24,067 comparaciones relevantes.
- Bajo control parcial por Speed y Stats_Total, esa ventaja cae a 49.92 por ciento en 605 casos.

### Interpretación

Eso sugiere que parte importante de la ventaja observada del doble tipo no es un efecto limpio del tipo adicional, sino una consecuencia de diferencias de atributos base asociadas a esos Pokemon.

### Riesgos y límites

- Las combinaciones de Type 1 y Type 2 generan mucha dispersión y muchas celdas escasas.
- Los perfiles de tipo más extremos pueden deberse a muestras pequeñas o nichos de enfrentamiento muy específicos.

### Conclusión del bloque

La información de tipos puede ser valiosa, pero conviene modelarla como información relacional o de interacción entre rivales, no como un ranking aislado de categorías. Es una fuente secundaria de señal, sensible a sparsity y a sobreinterpretación.

## 15. Resumen de relevancia de variables

El notebook sintetiza una jerarquía explícita de importancia:

- máxima prioridad para diferencias relativas entre oponentes,
- prioridad central para diff_speed y diff_total,
- relevancia adicional para diferencias ofensivas,
- utilidad auxiliar para Legendary, is_mega, Generation y Type,
- exclusión total de WinRate, Wins y n_combats del entrenamiento.

### Lectura metodológica

Este resumen es una pieza clave porque traduce el EDA en criterio de selección de variables y en diseño de la representación final del problema.

## 16. Riesgos para la validez del modelado

El notebook deja identificados varios riesgos metodológicos que no desaparecen por haber encontrado señal predictiva:

- fuga de información por métricas históricas derivadas del resultado,
- inflación del rendimiento por duplicados o enfrentamientos repetidos,
- confusión entre efectos de grupo y efectos de estadísticas base,
- sparsity en combinaciones raras de tipos,
- posible sesgo de construcción o de reglas implícitas detrás del peso extremo de Speed.

### Conclusión de esta sección

El mensaje es que encontrar asociaciones fuertes no basta. También hay que proteger la validez externa y la validez del esquema de evaluación.

## 17. Decisiones finales de preprocesamiento

El notebook propone como decisiones finales:

- eliminar batallas duplicadas exactas,
- trabajar con un target a nivel de batalla,
- tratar los nulos de Type 2 como ausencia estructural,
- excluir identificadores y métricas históricas contaminadas por el resultado,
- priorizar diferencias relativas como representación central,
- evaluar variables de grupo y de tipo solo como señales secundarias bajo validación libre de fuga.

## 18. Conclusión ejecutiva del EDA

La conclusión global del análisis es que la predicción del resultado de una batalla Pokemon debe apoyarse principalmente en comparaciones directas entre los dos oponentes, no en estadísticas históricas agregadas ni en etiquetas descriptivas leídas de forma aislada.

La señal dominante del notebook es la diferencia relativa de velocidad, seguida por la diferencia en estadísticas totales y por diferencias ofensivas. En cambio, variables como Legendary, Mega, Generation o Type contienen información útil pero secundaria, y buena parte de su aparente poder está mediado por las estadísticas base.

Desde el punto de vista metodológico, el notebook asume una postura prudente:

- rechaza variables con fuga de información,
- identifica duplicados como riesgo de validación,
- evita interpretar relaciones descriptivas como causalidad,
- y organiza el EDA en función de decisiones reales de modelado.

## Síntesis final en una sola lectura

Si este EDA se reduce a una idea central, sería la siguiente: para modelar correctamente las batallas, conviene representar cada combate como una comparación entre dos Pokemon y priorizar variables relativas como diff_speed y diff_total. Todo lo demás debe leerse alrededor de esa estructura principal y no por encima de ella.
