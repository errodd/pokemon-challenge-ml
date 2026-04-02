# EDA3: Explicacion de Conceptos y Analisis

## Conceptos estadisticos y metodologicos

### IC95 Wilson

El IC95 Wilson es un intervalo de confianza del 95% para una proporcion.

En este notebook lo usamos cuando una metrica es del tipo:

- porcentaje de victorias de un grupo,
- porcentaje de victorias de un matchup,
- porcentaje de ventaja de una categoria sobre otra.

Su objetivo es responder: si hoy observamos una proporcion muestral, cual es el rango plausible del valor real en la poblacion bajo incertidumbre muestral.

Por que usar Wilson y no solo la proporcion puntual:

- Porque un 80% con 20 observaciones no significa lo mismo que un 80% con 7,000 observaciones.
- Porque Wilson se comporta mejor que la aproximacion normal simple cuando la proporcion esta cerca de 0 o 1, o cuando el tamano muestral no es muy grande.
- Porque obliga a interpretar la precision del resultado y no solo su magnitud.

Interpretacion practica:

- Si un winrate es 73.35% con IC95 72.19%-74.49%, el resultado es bastante estable.
- Si un winrate es 36% con IC95 20.25%-55.48%, la incertidumbre es alta y no conviene sacar una conclusion fuerte.

En este notebook, el IC95 Wilson afecta directamente la lectura de los resultados porque evita sobreinterpretar diferencias observadas en grupos pequenos o matchups raros.

### Matchups dirigidos

Un matchup dirigido significa que no solo miramos que dos grupos se enfrentaron, sino quien esta en la fila y quien esta en la columna.

Ejemplo:

- fila: `Legendary`
- columna: `Normal`

El valor de la celda responde a:

- que porcentaje de veces gana el grupo de la fila cuando se enfrenta al grupo de la columna.

Esto es distinto de un conteo simetrico o una tabla no dirigida, porque:

- `Legendary vs Normal` no es lo mismo que `Normal vs Legendary`,
- la primera celda es el complemento de la segunda si solo hay dos resultados posibles.

Por que sirve:

- permite ver relaciones competitivas entre clases,
- facilita heatmaps interpretables,
- ayuda a detectar dominancia historica entre categorias.

Limite importante:

- si el conteo de una celda es bajo, el valor puede ser ruidoso.

Por eso en el notebook se acompanan los matchups dirigidos con matrices de conteo.

### Confusores

Un confusor es una variable que se relaciona con la variable explicativa y con el resultado al mismo tiempo.

Ejemplo en este dataset:

- `Legendary` puede parecer muy predictiva,
- pero los Pokemon legendarios tambien suelen tener mayor `Speed` y `Stats_Total`,
- entonces parte de la ventaja de `Legendary` puede venir realmente de esos stats y no de la etiqueta `Legendary` en si.

Eso significa que una asociacion bruta puede ser engañosa.

En este notebook se hizo un control parcial de confusores restringiendo la muestra a combates con:

- `|diff_speed| <= 5`
- `|diff_total| <= 30`

La logica es:

- si dos Pokemon son parecidos en `Speed` y `Stats_Total`,
- entonces la comparacion de grupo queda menos contaminada por esas diferencias.

Esto no elimina todos los confusores, pero mejora mucho la interpretacion.

## Como afectan estos conceptos al analisis

### Efecto sobre el analisis de legendarios y megas

Sin control, los grupos `Legendary` y `Mega` parecen muy fuertes porque su winrate historico es alto y tambien ganan muchos duelos cruzados.

Con control parcial por `Speed` y `Stats_Total`, la ventaja cae fuertemente.

Implicacion:

- la etiqueta del grupo contiene señal,
- pero una parte importante de esa señal parece estar mediada por stats base.

Conclusion metodologica:

- `Legendary` e `is_mega` son utiles como variables auxiliares,
- pero no deben interpretarse como causas directas de victoria sin ajuste multivariable.

### Efecto sobre el analisis de generacion

La generacion muestra diferencias pequenas en bruto y, cuando se controla parcialmente por stats, el efecto tiende a acercarse a 50%.

Implicacion:

- `Generation` probablemente funciona mas como variable contextual que como driver principal del resultado.

### Efecto sobre el analisis de tipos

Los tipos muestran asociaciones descriptivas interesantes en matchups dirigidos y en perfiles `Type1/Type2`.

Pero su lectura debe hacerse con cuidado porque:

- hay celdas con mucho desbalance de frecuencia,
- algunas combinaciones tienen pocos casos,
- los tipos pueden coexistir con Pokemon estructuralmente mas fuertes en stats.

Por eso el notebook combina:

- heatmaps de winrate,
- matrices de conteo,
- analisis single-type vs dual-type,
- control parcial por stats.

## Explicacion de los analisis del notebook

### 1. Data Audit

Objetivo:

- revisar estructura, tipos de variables, faltantes, duplicados y consistencia basica.

Que se hace:

- inspeccion de columnas y tipos de datos,
- deteccion de missing values,
- cuantificacion de duplicados,
- cardinalidad de campos,
- cobertura de IDs de combate contra la pokedex.

Para que sirve:

- identificar riesgos de leakage,
- evitar usar IDs como features nominales crudas,
- decidir que variables son numericas, categoricas o identificadores,
- detectar problemas que sesguen el modelado posterior.

Valor metodologico:

- un buen EDA empieza por saber si el dataset es estructuralmente confiable.

### 2. Analisis de la variable target

Objetivo:

- convertir el problema a una formulacion operativa de modelado.

Que se hace:

- se define `first_wins = 1` si gana el primer Pokemon,
- `first_wins = 0` si gana el segundo,
- se calcula la distribucion de clases,
- se estima una baseline ingenua,
- se mide la presencia de duplicados exactos.

Para que sirve:

- entender si hay imbalance severo,
- fijar una baseline minima de comparacion,
- anticipar sesgos de representacion por repeticion de combates.

Interpretacion:

- el target luce relativamente balanceado,
- por lo que accuracy sola no sera suficiente y no parece haber una clase totalmente dominante.

### 3. Relacion entre stats y probabilidad de ganar

Objetivo:

- medir cuanto aporta la ventaja relativa de stats entre oponentes.

Que se hace:

- se mapean stats de ambos Pokemon a cada combate,
- se construyen variables `diff_*`,
- se calcula correlacion con `first_wins`,
- se compara winrate cuando el primero tiene ventaja, empate o desventaja,
- se grafican deciles de diferencia.

Para que sirve:

- identificar drivers directos de victoria,
- justificar feature engineering basado en diferencias,
- detectar relaciones monotonicamente utiles para modelos.

Resultado conceptual fuerte:

- las diferencias entre oponentes son mas informativas que los valores aislados,
- `Speed` aparece como la senal dominante,
- `Stats_Total` y stats ofensivas tambien aportan.

### 4. Analisis de legendarios y megas

Objetivo:

- evaluar si ciertas clases de Pokemon concentran mejor rendimiento historico.

Que se hace:

- se crea `is_mega`,
- se forman grupos (`Normal`, `Mega`, `Legendary`, `Legendary + Mega`),
- se analizan medias historicas,
- se comparan duelos cruzados deduplicados,
- se agregan IC95 Wilson,
- se repite una comparacion controlada por `diff_speed` y `diff_total`.

Para que sirve:

- distinguir asociacion historica de posible confounding,
- decidir si `Legendary` e `is_mega` deben probarse como features del modelo.

Lectura correcta:

- hay asociacion bruta fuerte,
- pero parte de ella se reduce notablemente al controlar stats,
- por tanto estas variables no deben interpretarse solas.

### 5. Analisis de generacion

Objetivo:

- evaluar si el origen temporal o generacional del Pokemon tiene senal predictiva.

Que se hace:

- se construye `diff_generation`,
- se mide winrate del primero segun ventaja, empate o desventaja generacional,
- se construye matriz generacion vs generacion,
- se repite una comparacion controlada por stats.

Para que sirve:

- saber si `Generation` aporta informacion propia o solo contexto.

Lectura correcta:

- el efecto bruto es pequeno,
- y ajustado por stats se vuelve debil,
- por lo que `Generation` parece tener menor prioridad relativa para modelado.

### 6. Analisis de tipos

Objetivo:

- estudiar si `Type1`, `Type2` y sus combinaciones contienen senal competitiva historica.

Que se hace:

- se generan matchups dirigidos `Type1 vs Type1`,
- se construyen matrices de winrate y conteos,
- se estima winrate dirigido por `Type1`,
- se revisan perfiles `Type1/Type2`,
- se compara single-type vs dual-type en bruto y controlado.

Para que sirve:

- detectar relaciones estructurales de enfrentamiento,
- justificar features relacionales por tipo,
- decidir si conviene modelar tipos absolutos, combinaciones o interacciones entre oponentes.

Lectura correcta:

- los tipos muestran senal descriptiva,
- pero parte de su ventaja tambien puede estar mediada por stats,
- y las combinaciones raras no deben sobreinterpretarse.

## Que decision de modelado sugieren estos analisis

- Priorizar features relativas de combate: `diff_speed`, `diff_total`, `diff_attack`, etc.
- Mantener `Legendary`, `is_mega`, `Generation` y `Type` como candidatos secundarios.
- Evaluar estas variables por aporte incremental, no por interpretacion aislada.
- Hacer validacion con y sin duplicados, y con splits que reduzcan leakage por matchup repetido.
