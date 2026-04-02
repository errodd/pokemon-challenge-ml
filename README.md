# pokemon-challenge-ml

## Project Summary

This project aims to build a machine learning model that predicts the winner of a 1v1 Pokemon battle using structured data from a Pokedex table and a battle log.

The current phase is focused on **Exploratory Data Analysis (EDA)** to identify reliable predictive signals, detect data risks, and define robust preprocessing decisions before feature engineering and model training.

## Objective

Given two Pokemon in a battle (`First_pokemon`, `Second_pokemon`), predict the battle winner.

- Modeling unit: one battle
- Target for modeling: `first_wins` (binary)
- Task type: binary classification

## Data Sources

- `data/pokemon.csv`: Pokemon-level attributes (`HP`, `Attack`, `Defense`, `Sp. Atk`, `Sp. Def`, `Speed`, `Type 1`, `Type 2`, `Generation`, `Legendary`)
- `data/combats.csv`: battle records (`First_pokemon`, `Second_pokemon`, `Winner`)

## Current Status (EDA)

The EDA work is concentrated in `notebooks/EDA.ipynb` as the final analysis notebook. Main outcomes so far:

- Structural data audit completed (types, missingness, duplicates, coverage checks)
- Initial cardinality and feature-role analysis completed
- Target definition and class behavior analysis completed
- Clear separation between descriptive metrics and training-safe features
- Strong evidence that **relative stat differences** are central predictive signals
- Risk identification completed (leakage, repeated battles, high-cardinality identifiers)

## Repository Structure

- `notebooks/EDA.ipynb`: final professional EDA notebook (active)
- `data/`: raw datasets
- `reports/figures/`: exported EDA visualizations
- `01_eda.ipynb`, `02_data_preparation.ipynb`: workflow support notebooks

## Next Step

The next project stage is **Feature Engineering**, where EDA conclusions will be transformed into model-ready battle-level features and validated with leakage-safe evaluation.

Planned improvements include:

- Feature construction from relative Pokemon attributes
- Encoding strategy for categorical variables with controlled cardinality
- Validation-aware transformation pipeline
- Preparation for baseline and advanced classification models