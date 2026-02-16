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
## Requerimientos
**Funcionalidad**
- Tabla de tipos de debilidades y resistencias básica
- (opcional) Tabla de debilidades y resistencia * tipo y combinaciones
**Histogramas:**
- GENERAL Pokémon por tipo Total (X=Tipo=18, Y=Cantidad)
- GENERAL Pokémon por generación Total (X=gen, Y=Cantidad)
- Por cada tipo: Cantidad de Pokémon por generación (18* X=generación=6, Y=Cantidad)
- Por cada tipo: Cantidad de Pokémon por combinación (18* X=Combinación<=18, Y=Cantidad)
- Por cada generación: Cantidad de Pokémon por tipo (6* X=Tipo=18, Y=Cantidad)
**Gráfica**
- Cuántos Pokémon con doble 2 tipos 
- Cuántos Pokémon con 1 único tipo
- Cuántos legendarios hay
**Mapa de calor:**
- Tipos que más ganan batallas (X=Tipo, Y=Cantidad)
- Generaciones que más ganan (X=Generación, Y=Cantidad)
**Tablas**
- Cuáles son los 100 o 50 o 25 o 10 pokémones que más batallas ganan (Serie auxiliar de victorias por Pokémon y dataset de mejores Pokémon)
- Top 25 Mejores Pokémon x característica (+HP, +Atk, +Def, +AtkSP, +DefSP, +Spd)