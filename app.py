"""Gradio web application for the Pokemon battle winner predictor.

Launch with:
    python app.py

or using the Gradio CLI:
    gradio app.py
"""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

from src.predict import load_resources, predict_battle

# ---------------------------------------------------------------------------
# Load resources once at startup
# ---------------------------------------------------------------------------
_pokemon_df, _pokedex, _model = load_resources()
_pokemon_names: list[str] = sorted(_pokemon_df["Name"].tolist())

_MODEL_CARD_PATH = Path(__file__).resolve().parent / "artifacts" / "model_card_pokemon.json"
with open(_MODEL_CARD_PATH, encoding="utf-8") as _f:
    _model_card = json.load(_f)

_accuracy = _model_card["test_metrics"]["accuracy"]
_roc_auc = _model_card["test_metrics"]["roc_auc"]


# ---------------------------------------------------------------------------
# Prediction callback
# ---------------------------------------------------------------------------
def _predict(first_name: str, second_name: str) -> tuple[str, str, str]:
    """Run the battle prediction and return formatted outputs."""
    if not first_name or not second_name:
        return "⚠️ Please select both Pokemon.", "", ""

    if first_name == second_name:
        return "⚠️ Please select two different Pokemon.", "", ""

    result = predict_battle(first_name, second_name, _pokemon_df, _pokedex, _model)

    winner = result["winner"]
    prob_first = result["probability_first_wins"]
    prob_second = result["probability_second_wins"]

    # Winner banner
    if result["first_wins"]:
        banner = f"🏆 **{first_name}** wins!"
    else:
        banner = f"🏆 **{second_name}** wins!"

    # Confidence
    confidence = f"Confidence: **{max(prob_first, prob_second) * 100:.1f}%**"

    # Stats comparison table (Markdown)
    first_stats = result["first_stats"]
    second_stats = result["second_stats"]
    stats_keys = list(first_stats.keys())

    rows = "| Stat | " + first_name + " | " + second_name + " |\n"
    rows += "|------|" + "-------|" * 2 + "\n"
    for stat in stats_keys:
        v1 = first_stats[stat]
        v2 = second_stats[stat]
        marker1 = " ✅" if v1 > v2 else ""
        marker2 = " ✅" if v2 > v1 else ""
        rows += f"| {stat} | {v1}{marker1} | {v2}{marker2} |\n"

    total1 = sum(first_stats.values())
    total2 = sum(second_stats.values())
    marker1 = " ✅" if total1 > total2 else ""
    marker2 = " ✅" if total2 > total1 else ""
    rows += f"| **Total** | **{total1}**{marker1} | **{total2}**{marker2} |\n"

    return banner, confidence, rows


# ---------------------------------------------------------------------------
# Gradio interface
# ---------------------------------------------------------------------------
with gr.Blocks(title="Pokemon Battle Predictor") as demo:
    gr.Markdown(
        f"""
# ⚔️ Pokemon Battle Predictor

Select two Pokemon and the model will predict who wins the 1v1 battle.

> Model: HistGradientBoosting — Test Accuracy **{_accuracy * 100:.1f}%** · ROC-AUC **{_roc_auc * 100:.1f}%**
"""
    )

    with gr.Row():
        first_pokemon = gr.Dropdown(
            choices=_pokemon_names,
            label="🥊 First Pokemon",
            value="Pikachu",
        )
        second_pokemon = gr.Dropdown(
            choices=_pokemon_names,
            label="🥊 Second Pokemon",
            value="Mewtwo",
        )

    predict_btn = gr.Button("⚔️ Predict Battle", variant="primary")

    with gr.Column():
        winner_output = gr.Markdown(label="Result")
        confidence_output = gr.Markdown(label="Confidence")
        stats_output = gr.Markdown(label="Stats Comparison")

    predict_btn.click(
        fn=_predict,
        inputs=[first_pokemon, second_pokemon],
        outputs=[winner_output, confidence_output, stats_output],
    )

    gr.Markdown(
        """
---
### How it works

The model uses **relational battle features** derived from each Pokemon's base stats
(HP, Attack, Defense, Sp. Atk, Sp. Def, Speed), type, generation, and legendary status.

It was trained on ~50 000 historical battles using a HistGradientBoosting classifier
with 5-fold cross-validated hyperparameter tuning.
"""
    )

if __name__ == "__main__":
    demo.launch()
