"""Prediction module for the Pokemon battle winner predictor.

Exposes two public helpers:
- ``load_resources()``  – load the Pokedex and the trained pipeline once.
- ``predict_battle()``  – given two Pokemon names return the prediction result.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from scipy import sparse


# ---------------------------------------------------------------------------
# The trained pipeline was serialised in a Jupyter notebook where
# ``densify_if_sparse`` lived in ``__main__``.  We must re-inject it there
# before calling ``joblib.load`` so pickle can resolve the reference.
# ---------------------------------------------------------------------------
def densify_if_sparse(x: Any) -> Any:
    """Return a dense array; pass through if the input is already dense."""
    return x.toarray() if sparse.issparse(x) else x


sys.modules["__main__"].__dict__["densify_if_sparse"] = densify_if_sparse

# ---------------------------------------------------------------------------
# Paths – resolved relative to this file so the module works from any cwd.
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent.parent
_POKEMON_CSV = _ROOT / "data" / "pokemon.csv"
_MODEL_PATH = _ROOT / "artifacts" / "final_model_pipeline_pokemon.joblib"

STATS_COLS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _make_unordered_pair(a: str, b: str) -> str:
    return "|".join(sorted([str(a), str(b)]))


def _build_pokedex(pokemon_df: pd.DataFrame) -> pd.DataFrame:
    """Return an ID-indexed DataFrame with normalised Pokemon attributes."""
    lookup = pokemon_df.copy()
    lookup["Type 2"] = lookup["Type 2"].fillna("None")
    lookup["is_mega"] = lookup["Name"].str.contains(r"Mega|Primal", case=False, na=False).astype(int)
    lookup["Legendary"] = lookup["Legendary"].astype(int)
    lookup["stats_total"] = lookup[STATS_COLS].sum(axis=1)
    return lookup.set_index("#")


def _build_battle_features(first_id: int, second_id: int, pokedex: pd.DataFrame) -> pd.DataFrame:
    """Build a single-row DataFrame of battle-level features for the pipeline."""
    fields = STATS_COLS + ["stats_total", "Type 1", "Type 2", "Generation", "Legendary", "is_mega"]

    first_row = pokedex.loc[first_id, fields]
    second_row = pokedex.loc[second_id, fields]

    row: Dict[str, Any] = {}

    for col in fields:
        row[f"first_{col}"] = first_row[col]
        row[f"second_{col}"] = second_row[col]

    # Relative continuous features.
    for col in STATS_COLS + ["stats_total"]:
        safe = col.lower().replace(". ", "_").replace(" ", "_")
        row[f"diff_{safe}"] = row[f"first_{col}"] - row[f"second_{col}"]
        row[f"abs_diff_{safe}"] = abs(row[f"diff_{safe}"])
        row[f"first_has_adv_{safe}"] = int(row[f"diff_{safe}"] > 0)

    # Relative binary/contextual features.
    row["diff_generation"] = row["first_Generation"] - row["second_Generation"]
    row["diff_legendary"] = row["first_Legendary"] - row["second_Legendary"]
    row["diff_is_mega"] = row["first_is_mega"] - row["second_is_mega"]

    row["same_type1"] = int(row["first_Type 1"] == row["second_Type 1"])
    row["same_type2"] = int(row["first_Type 2"] == row["second_Type 2"])
    row["same_generation"] = int(row["first_Generation"] == row["second_Generation"])
    row["both_legendary"] = int(row["first_Legendary"] == 1 and row["second_Legendary"] == 1)

    row["type1_pair"] = _make_unordered_pair(row["first_Type 1"], row["second_Type 1"])
    row["type2_pair"] = _make_unordered_pair(row["first_Type 2"], row["second_Type 2"])

    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def load_resources() -> Tuple[pd.DataFrame, pd.DataFrame, Any]:
    """Load and return (pokemon_df, pokedex, model_pipeline).

    Call this once at startup to avoid repeated I/O.
    """
    pokemon_df = pd.read_csv(_POKEMON_CSV)
    pokedex = _build_pokedex(pokemon_df)
    model = joblib.load(_MODEL_PATH)
    return pokemon_df, pokedex, model


def predict_battle(
    first_name: str,
    second_name: str,
    pokemon_df: pd.DataFrame,
    pokedex: pd.DataFrame,
    model: Any,
) -> Dict[str, Any]:
    """Predict the winner of a 1v1 Pokemon battle.

    Parameters
    ----------
    first_name, second_name:
        Pokemon names exactly as they appear in the dataset.
    pokemon_df:
        Raw pokemon DataFrame (used only for name → ID lookup).
    pokedex:
        ID-indexed lookup table produced by ``load_resources()``.
    model:
        Trained sklearn Pipeline.

    Returns
    -------
    dict with keys:
        ``first_wins`` (bool), ``winner`` (str), ``probability_first_wins`` (float),
        ``probability_second_wins`` (float), ``first_stats`` (dict), ``second_stats`` (dict).
    """
    name_to_id = pokemon_df.set_index("Name")["#"].to_dict()

    if first_name not in name_to_id:
        raise ValueError(f"Pokemon not found: '{first_name}'")
    if second_name not in name_to_id:
        raise ValueError(f"Pokemon not found: '{second_name}'")

    first_id = int(name_to_id[first_name])
    second_id = int(name_to_id[second_name])

    features = _build_battle_features(first_id, second_id, pokedex)

    pred = int(model.predict(features)[0])
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        prob_first = float(proba[1])
    else:
        prob_first = 1.0 if pred == 1 else 0.0

    winner = first_name if pred == 1 else second_name

    def _stats(pokemon_id: int) -> Dict[str, Any]:
        row = pokedex.loc[pokemon_id]
        return {stat: int(row[stat]) for stat in STATS_COLS}

    return {
        "first_wins": bool(pred),
        "winner": winner,
        "probability_first_wins": prob_first,
        "probability_second_wins": round(1.0 - prob_first, 4),
        "first_stats": _stats(first_id),
        "second_stats": _stats(second_id),
    }
