# Pokemon - Data Preparation & Feature Engineering (Transcripcion completa)

Este documento transcribe toda la informacion del notebook notebooks/Data Preparation.ipynb en formato Markdown, manteniendo el orden original de celdas.

## Celda 1 (Markdown)

<img src="logos/logo_Facyt.png"
     width="250"
     style="display: block; margin-left: auto; margin-right: auto;">

# Pokemon - Data Preparation & Feature Engineering (Industrial Standard)

Este notebook construye una fase de preparacion de datos profesional para modelar batallas Pokemon.

Principios clave:
- Definir el target a nivel batalla (`first_wins`).
- Separar train/test antes de cualquier ajuste de pipeline.
- Evitar leakage (no usar `Winner`, `WinRate`, `Wins`, `n_combats`).
- Usar `Pipeline` y `ColumnTransformer` para transformaciones reproducibles.
- Persistir artefactos para el siguiente notebook de modelado.

## Celda 2 (Markdown)

## 1) Imports y configuracion

## Celda 3 (Codigo)

```python
from pathlib import Path

import json
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Alineada con EDA para mayor reproducibilidad transversal
RANDOM_STATE = 29
TEST_SIZE = 0.20
DATA_DIR = Path("../data")
ARTIFACTS_DIR = Path("../artifacts")
TARGET_COL = "first_wins"

pd.set_option("display.max_columns", 200)
pd.set_option("display.width", 140)
```

## Celda 4 (Markdown)

## 2) Carga de datos
Se cargan las tablas base de Pokedex y combates.

## Celda 5 (Codigo)

```python
pokemon_path = DATA_DIR / "pokemon.csv"
combats_path = DATA_DIR / "combats.csv"

pokemon_df = pd.read_csv(pokemon_path)
combats_df = pd.read_csv(combats_path)

print(f"pokemon_df shape: {pokemon_df.shape}")
print(f"combats_df shape: {combats_df.shape}")
display(pokemon_df.head(3))
display(combats_df.head(3))
```

## Celda 6 (Markdown)

## 3) Auditoria minima y reglas anti-leakage
Validamos estructura minima y declaramos variables prohibidas para entrenamiento.

## Celda 7 (Codigo)

```python
required_pokemon_cols = {
    "#", "Name", "Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Generation", "Legendary"
}
required_combats_cols = {"First_pokemon", "Second_pokemon", "Winner"}

missing_pokemon_cols = sorted(required_pokemon_cols.difference(pokemon_df.columns))
missing_combats_cols = sorted(required_combats_cols.difference(combats_df.columns))

if missing_pokemon_cols:
    raise ValueError(f"Faltan columnas en pokemon_df: {missing_pokemon_cols}")
if missing_combats_cols:
    raise ValueError(f"Faltan columnas en combats_df: {missing_combats_cols}")

LEAKAGE_COLUMNS = {"Winner", "WinRate", "Wins", "n_combats"}
print("Columnas de leakage prohibidas como features:", sorted(LEAKAGE_COLUMNS))

pokemon_ids = set(pokemon_df["#"].astype(int))
combat_ids = set(combats_df["First_pokemon"]).union(set(combats_df["Second_pokemon"]))
coverage = len(combat_ids.intersection(pokemon_ids)) / len(combat_ids)
print(f"Cobertura de IDs de combate dentro de Pokedex: {coverage * 100:.2f}%")
```

## Celda 8 (Markdown)

## 4) Limpieza estructural
Se eliminan duplicados exactos y se normalizan campos base.

## Celda 9 (Codigo)

```python
initial_rows = len(combats_df)
combats_df = combats_df.drop_duplicates(subset=["First_pokemon", "Second_pokemon", "Winner"]).copy()
removed_duplicates = initial_rows - len(combats_df)

pokemon_df = pokemon_df.copy()
pokemon_df["Type 2"] = pokemon_df["Type 2"].fillna("None")
pokemon_df["is_mega"] = pokemon_df["Name"].str.contains(r"Mega|Primal", case=False, na=False).astype(int)
pokemon_df["Legendary"] = pokemon_df["Legendary"].astype(int)

print(f"Combates originales: {initial_rows:,}")
print(f"Combates tras deduplicar: {len(combats_df):,}")
print(f"Duplicados eliminados: {removed_duplicates:,}")
```

## Celda 10 (Markdown)

## 5) Funciones de feature engineering
Se construyen features a nivel batalla para representar ambos contendientes y sus diferencias.

## Celda 11 (Codigo)

```python
STATS_COLS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]


def build_pokedex_lookup(pokemon_frame: pd.DataFrame) -> pd.DataFrame:
    """Crea tabla indexada por id para joins rapidos en combates."""
    lookup = pokemon_frame.copy()
    lookup["stats_total"] = lookup[STATS_COLS].sum(axis=1)
    return lookup.set_index("#")


def build_battle_level_dataset(combats_frame: pd.DataFrame, pokedex_lookup: pd.DataFrame) -> pd.DataFrame:
    """Construye dataset de modelado a nivel batalla con target y features de ambos Pokemon."""
    base = combats_frame[["First_pokemon", "Second_pokemon", "Winner"]].copy()
    base["first_wins"] = (base["Winner"] == base["First_pokemon"]).astype(int)

    # Clave de pareja no ordenada para split dependency-aware
    base["matchup_key"] = base.apply(
        lambda r: f"{min(r['First_pokemon'], r['Second_pokemon'])}_{max(r['First_pokemon'], r['Second_pokemon'])}",
        axis=1,
    )

    fields = STATS_COLS + ["stats_total", "Type 1", "Type 2", "Generation", "Legendary", "is_mega"]

    for prefix, id_col in [("first", "First_pokemon"), ("second", "Second_pokemon")]:
        mapped = pokedex_lookup.loc[:, fields].reindex(base[id_col]).reset_index(drop=True)
        mapped.columns = [f"{prefix}_{c}" for c in mapped.columns]
        base = pd.concat([base.reset_index(drop=True), mapped], axis=1)

    # Control de integridad posterior al join
    join_cols = [f"first_{c}" for c in fields] + [f"second_{c}" for c in fields]
    missing_join_rows = int(base[join_cols].isna().any(axis=1).sum())
    if missing_join_rows > 0:
        raise ValueError(
            f"Se detectaron {missing_join_rows} filas con joins incompletos. Revisar cobertura de IDs en Pokedex."
        )

    for col in STATS_COLS + ["stats_total"]:
        safe_col = col.lower().replace(". ", "_").replace(" ", "_")
        base[f"diff_{safe_col}"] = base[f"first_{col}"] - base[f"second_{col}"]
        base[f"abs_diff_{safe_col}"] = base[f"diff_{safe_col}"].abs()

    base["same_type1"] = (base["first_Type 1"] == base["second_Type 1"]).astype(int)
    base["same_type2"] = (base["first_Type 2"] == base["second_Type 2"]).astype(int)
    base["same_generation"] = (base["first_Generation"] == base["second_Generation"]).astype(int)
    base["both_legendary"] = ((base["first_Legendary"] == 1) & (base["second_Legendary"] == 1)).astype(int)

    return base
```

## Celda 12 (Markdown)

## 6) Construir dataset final de preparacion

## Celda 13 (Codigo)

```python
pokedex_lookup = build_pokedex_lookup(pokemon_df)
battle_df = build_battle_level_dataset(combats_df, pokedex_lookup)

print(f"battle_df shape: {battle_df.shape}")
display(battle_df.head(3))
```

## Celda 14 (Markdown)

## 7) Definicion de target y split dependency-aware
La separacion se hace antes de ajustar cualquier transformacion y evitando fuga por emparejamientos repetidos.

## Celda 15 (Codigo)

```python
X = battle_df.drop(columns=[TARGET_COL])
y = battle_df[TARGET_COL].astype(int)

# Split por grupos de emparejamiento (pareja no ordenada) para reducir dependencia train-test
gss = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=RANDOM_STATE)
train_idx, test_idx = next(gss.split(X, y, groups=X["matchup_key"]))

X_train = X.iloc[train_idx].copy()
X_test = X.iloc[test_idx].copy()
y_train = y.iloc[train_idx].copy()
y_test = y.iloc[test_idx].copy()

# Chequeo de no solapamiento de grupos entre train y test
train_groups = set(X_train["matchup_key"])
test_groups = set(X_test["matchup_key"])
group_overlap = len(train_groups.intersection(test_groups))

print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")
print(f"Target train mean: {y_train.mean():.4f}")
print(f"Target test mean: {y_test.mean():.4f}")
print(f"Group overlap (debe ser 0): {group_overlap}")
```

## Celda 16 (Markdown)

## 8) Feature selection y tipado
Se excluyen identificadores y columnas con leakage.

## Celda 17 (Codigo)

```python
id_like_cols = ["First_pokemon", "Second_pokemon", "Winner", "matchup_key"]
leakage_cols = sorted(LEAKAGE_COLUMNS.intersection(X_train.columns))
drop_cols = [c for c in id_like_cols + leakage_cols if c in X_train.columns]

X_train_fe = X_train.drop(columns=drop_cols, errors="ignore").copy()
X_test_fe = X_test.drop(columns=drop_cols, errors="ignore").copy()

numeric_features = [
    c for c in X_train_fe.columns
    if c.startswith("diff_") or c.startswith("abs_diff_") or c in ["first_stats_total", "second_stats_total"]
]

categorical_features = [
    c for c in ["first_Type 1", "second_Type 1", "first_Type 2", "second_Type 2", "first_Generation", "second_Generation"]
    if c in X_train_fe.columns
]

binary_features = [
    c for c in ["first_Legendary", "second_Legendary", "first_is_mega", "second_is_mega", "same_type1", "same_type2", "same_generation", "both_legendary"]
    if c in X_train_fe.columns
]

print("Total features tras limpieza:", X_train_fe.shape[1])
print("Numeric:", len(numeric_features))
print("Categorical:", len(categorical_features))
print("Binary:", len(binary_features))
```

## Celda 18 (Markdown)

## 9) Arquitectura de preprocessing
`ColumnTransformer` permite procesar cada tipo de feature con su estrategia correcta.

## Celda 19 (Codigo)

```python
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocess_pipeline = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
        ("bin", "passthrough", binary_features),
    ],
    remainder="drop",
)

preprocess_pipeline
```

## Celda 20 (Markdown)

## 10) Validacion tecnica del pipeline
Se ajusta solo con train y se transforma train/test para verificar consistencia.

## Celda 21 (Codigo)

```python
X_train_transformed = preprocess_pipeline.fit_transform(X_train_fe)
X_test_transformed = preprocess_pipeline.transform(X_test_fe)

print("Transformed train shape:", X_train_transformed.shape)
print("Transformed test shape:", X_test_transformed.shape)
print("Nulls en y_train:", int(y_train.isna().sum()))
print("Nulls en y_test:", int(y_test.isna().sum()))
```

## Celda 22 (Markdown)

## 11) Matrices finales para modelado
Se exponen objetos base para la siguiente fase de entrenamiento.

## Celda 23 (Codigo)

```python
X_train_final = X_train_fe.copy()
X_test_final = X_test_fe.copy()

print("X_train_final:", X_train_final.shape)
print("X_test_final:", X_test_final.shape)
```

## Celda 24 (Markdown)

## 12) Persistencia de artefactos
Se guardan pipeline, split y manifiesto de features para reproducibilidad.

## Celda 25 (Codigo)

```python
import joblib

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(preprocess_pipeline, ARTIFACTS_DIR / "preprocess_pipeline_pokemon.joblib")
joblib.dump((X_train_final, X_test_final, y_train, y_test), ARTIFACTS_DIR / "split_data_pokemon.joblib")

feature_manifest = {
    "target": TARGET_COL,
    "drop_cols": drop_cols,
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "binary_features": binary_features,
    "notes": [
        "No se usan Winner/WinRate/Wins/n_combats como features por leakage.",
        "Se elimino duplicado exacto de combates antes de feature engineering.",
        "Type 2 se interpreta como ausencia estructural con valor None."
    ]
}

with open(ARTIFACTS_DIR / "feature_manifest_pokemon.json", "w", encoding="utf-8") as f:
    json.dump(feature_manifest, f, ensure_ascii=False, indent=2)

print("Artefactos guardados en:", ARTIFACTS_DIR.resolve())
```

## Celda 26 (Markdown)

## 13) Output summary
Este notebook produce:
- `X_train_final`, `X_test_final`, `y_train`, `y_test`
- `preprocess_pipeline` (fiteado sobre train)
- `../artifacts/preprocess_pipeline_pokemon.joblib`
- `../artifacts/split_data_pokemon.joblib`
- `../artifacts/feature_manifest_pokemon.json`

Ajustes metodologicos aplicados en esta version:
- Split dependency-aware por pareja de combate (`matchup_key`) para reducir fuga por dependencia.
- Verificacion explicita de no solapamiento de grupos entre train y test.
- Control de integridad post-join para detectar filas sin mapeo del Pokedex.
- Semilla alineada con EDA para consistencia de resultados entre fases.

## Celda 27 (Markdown)

## 14) Guia rapida de estudio (resumen)
Conceptos tecnicos que debes dominar para esta fase:
- Unidad de analisis: una fila = una batalla.
- Variable objetivo: `first_wins`.
- Leakage: cualquier variable derivada de resultados historicos globales.
- Feature engineering relacional: modelar diferencias entre oponentes (`diff_*`).
- Validacion dependency-aware: evitar que el mismo emparejamiento aparezca en train y test.
- Preprocessing por tipo: numericas, categoricas, binarias.
- Reproducibilidad: versionado, pipeline serializado y manifiesto de features.

Para estudio extendido, consulta el archivo `reports/guia_data_preparation_pokemon.md`.
