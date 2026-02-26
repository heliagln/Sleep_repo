from __future__ import annotations


import os
import sys
import re
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from sleep_score import *


FILENAME_DATE_RE = re.compile(r"^(?P<y>\d{2})(?P<m>\d{2})(?P<d>\d{2})_.*\.csv$", re.IGNORECASE)

def parse_date_from_filename(filename: str) -> pd.Timestamp | None:
    """
    Parse '260207_....csv' -> Timestamp('2026-02-07')
    Suppose format = YYMMDD_...
    """
    m = FILENAME_DATE_RE.match(filename)
    if not m:
        return None
    yy = int(m.group("y"))
    mm = int(m.group("m"))
    dd = int(m.group("d"))
    # Hypothèse : 20YY (donc 26 -> 2026)
    return pd.Timestamp(year=2000 + yy, month=mm, day=dd)

def compute_daily_scores(
    input_dir: str | Path,
    output_csv: str | Path,
    age: float,
    age_csv: str | Path,
    recommendation_csv: str | Path,
    fill_missing_days: bool = True,
    file_glob: str = "*_garmin-connect-sleep-stage_*.csv",
) -> pd.DataFrame:
    input_dir = Path(input_dir)
    files = sorted(input_dir.glob(file_glob))

    rows = []
    for fp in files:
        day = parse_date_from_filename(fp.name)
        if day is None:
            # Fichier qui ne matche pas le pattern; on ignore
            continue

        try:
            score = sleep_score_value(fp, age=age, age_csv=age_csv, recommendation_csv=recommendation_csv)  # <-- ta fonction appelée ici
        except Exception as e:
            # Si tu préfères "planter" au lieu de continuer, remplace par: raise
            print(f"[WARN] Impossible de scorer {fp.name}: {e}")
            score = pd.NA

        rows.append({"date": day.date().isoformat(), "score": score, "file": fp.name})

    df = pd.DataFrame(rows)

    if df.empty:
        # Crée quand même un CSV vide propre
        df = pd.DataFrame(columns=["date", "score"])
        df.to_csv(output_csv, index=False)
        return df

    # S'il y a plusieurs fichiers pour la même date, on garde le dernier (ou adapte si besoin)
    df = df.sort_values(["date", "file"]).drop_duplicates(subset=["date"], keep="last")

    if fill_missing_days:
        # Convertit la colonne "date" (string) en datetime
        df["_date_dt"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["_date_dt"])

        full_range = pd.date_range(df["_date_dt"].min(), df["_date_dt"].max(), freq="D")

        # On enlève l'ancienne colonne "date" pour éviter les collisions
        df = df.drop(columns=["date"])

        # Reindex sur la plage complète
        df = df.set_index("_date_dt").reindex(full_range)

        # IMPORTANT: s'assurer que l'index se nomme "date"
        df.index.name = "date"

        # Revenir en colonnes
        df = df.reset_index()

        # À ce stade, la colonne s'appelle bien "date"
        df["date"] = df["date"].dt.date.astype(str)

        # Optionnel: virer la colonne file si tu l'avais gardée
        # if "file" in df.columns: df = df.drop(columns=["file"])

    # On ne garde que date, score (forme demandée)
    out = df[["date", "score"]].copy()
    out.to_csv(output_csv, index=False)
    return out

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Compute the sleep score based on the provided sleep data CSV file."
    )
    parser.add_argument(
        "sleep_csv_folder",
        type=str,
        help="Path to the folder sleep data CSV files.",
    )
    parser.add_argument(
        "output_csv",
        type=str,
        help="Path to the output CSV file for daily scores.",
    )
    parser.add_argument(
        "-age",
        type=float,
        help="Age of the subject.",
    )
    parser.add_argument(
        "--age_csv",
        type=str,
        required=False,
        default="age.csv",
        help="Path to the age CSV file.",
    )
    parser.add_argument(
        "--recommendation_csv",
        type=str,
        required=False,
        default="reco_sleep_quality.csv",
        help="Path to the sleep recommendation CSV file.",
    )
    args = parser.parse_args()

    compute_daily_scores(
        input_dir=args.sleep_csv_folder,
        output_csv=args.output_csv,
        age=args.age,
        age_csv=args.age_csv,
        recommendation_csv=args.recommendation_csv
    )