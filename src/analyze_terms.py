"""
analyze_terms.py
-----------------
Dieses Skript führt die Keyword-Frequenzanalyse und Zeitreihenaggregation durch.

Abhängigkeiten:
- data/processed/combined_texts.json
- data/term_list.json
- utils.py
"""

import json
import re
import pandas as pd
from utils import load_json, save_csv

# TODO:
# 1. Keywords aus data/term_list.json laden
# 2. Texte aus data/processed/combined_texts.json laden
# 3. Frequenzen pro Jahr und Cluster zählen
# 4. Ergebnisse als yearly_keyword_counts.csv und yearly_cluster_sums.csv speichern
# 5. Verhältnisindikator R_t berechnen und speichern

def analyze_terms():
    """
    Zählt definierte Keywords und erstellt jährliche Statistiken.
    """
    term_data = load_json("data/term_list.json")
    combined_texts = load_json("data/processed/combined_texts.json")

    records = []

    for document in combined_texts:
        jahr = document.get("jahr")
        if jahr is None:
            continue

        text = document.get("text", "")
        for cluster, cluster_info in term_data.items():
            keywords = cluster_info.get("keywords", [])
            for keyword in keywords:
                pattern = re.compile(rf"\b{re.escape(keyword)}\b", flags=re.IGNORECASE)
                count = len(pattern.findall(text))
                if count > 0:
                    records.append(
                        {
                            "year": jahr,
                            "cluster": cluster,
                            "keyword": keyword,
                            "count": count,
                        }
                    )

    if not records:
        keyword_counts_df = pd.DataFrame(columns=["year", "cluster", "keyword", "count"])
    else:
        keyword_counts_df = pd.DataFrame(records)
        keyword_counts_df = (
            keyword_counts_df.groupby(["year", "cluster", "keyword"], as_index=False)["count"].sum()
        )

    cluster_sums_df = (
        keyword_counts_df.groupby(["year", "cluster"], as_index=False)["count"].sum()
        if not keyword_counts_df.empty
        else pd.DataFrame(columns=["year", "cluster", "count"])
    )

    pivot = cluster_sums_df.pivot(index="year", columns="cluster", values="count") if not cluster_sums_df.empty else pd.DataFrame()
    pivot = pivot.fillna(0)

    resilience_series = pivot.get("sicherheit_resilienz", pd.Series(0, index=pivot.index))
    ecology_series = pivot.get("oekologie_nachhaltigkeit", pd.Series(0, index=pivot.index))

    ratio_series = resilience_series.divide(ecology_series.replace(0, pd.NA))
    relative_ratios_df = pd.DataFrame(
        {
            "year": pivot.index,
            "ratio": ratio_series,
            "sicherheit_resilienz": resilience_series,
            "oekologie_nachhaltigkeit": ecology_series,
        }
    ).reset_index(drop=True)

    save_csv(keyword_counts_df, "data/results/yearly_keyword_counts.csv")
    save_csv(cluster_sums_df, "data/results/yearly_cluster_sums.csv")
    save_csv(relative_ratios_df, "data/results/relative_ratios.csv")

if __name__ == "__main__":
    analyze_terms()
