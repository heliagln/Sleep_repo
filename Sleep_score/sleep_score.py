import sys
import argparse
import numpy as np
import pandas as pd

def extract_category(age: int, age_data: pd.DataFrame) -> str:
    # Extract the age category based on the provided age and age data
    age_data.sort_values(by=["age"])
    min_category = age_data[age < age_data["age"]]
    category = age_data.iloc[min_category["age"].idxmin()]["age_category"]
    return category

def compute_sleep_percent(stage: str, sleep_data: pd.DataFrame, total_time: float) -> float:
    # Compute the percentage of time spent in a specific sleep stage
    stage_time = sleep_data[sleep_data["type"] == stage]["durationInMs"].sum() # in ms
    return stage_time / total_time * 100

def computes_indicators(sleep_data: pd.DataFrame, reco_age: pd.DataFrame) -> int:
    # Compute the sleep score based on the sleep data and recommendation data
    sleep_score = 0
    total_time = sleep_data["durationInMs"].sum() # in ms
    indicators = {}
    for _, row in reco_age.iterrows():
        # Separate the name of indicators
        indicator_name_split = row["indicator"].split("_")
        if indicator_name_split[1] == "sleep" and indicator_name_split[2] == "percent":
            indicator_score = compute_sleep_percent(indicator_name_split[0], sleep_data[sleep_data["type"] == indicator_name_split[0]], total_time)
            indicators[row["indicator"]] = indicator_score
        elif indicator_name_split[0] == "awakenings":
            indicator_score = sleep_data[(sleep_data["type"] == "awake") & (sleep_data["durationInMs"] >= 5 * 60 * 1000)]["durationInMs"].count()
            indicators[row["indicator"]] = indicator_score
        elif indicator_name_split[0] == "wake":
            indicator_score = sleep_data[sleep_data["type"] == "awake"]["durationInMs"].sum() / total_time * 100
            indicators[row["indicator"]] = indicator_score
        else:
            indicators[row["indicator"]] = total_time / (1000 * 60 * 60) # in hours
    return indicators

def compute_score_for_row(row: pd.Series, values: dict):
    # Separate tje couples (max_i, score_i) in the recommendation data
    pairs = []
    i = 1
    max_score = 0
    while f"max_{i}" in row or f"score_{i}" in row:
        mx = row[f"max_{i}"]
        sc = row[f"score_{i}"]
        if pd.notna(sc):  # score doit exister
            pairs.append((mx, int(sc)))
            max_score = max(max_score, int(sc))
        i += 1
    
    fallback_score = 0
    for mx, sc in pairs:
        if pd.isna(mx):
            # "au-delà" (NaN) => fallback
            fallback_score = sc
        else:
            if values <= float(mx):
                return sc, max_score

    # Si aucune borne numérique n'a matché
    if fallback_score is not None:
        return fallback_score, max_score

    # Sinon, dernier score connu (cas rare si pas de NaN)
    return (pairs[-1][1], max_score) if pairs else (0, max_score)

def compute_sleep_score(reco_age: pd.DataFrame, indicators: dict) -> int:
    # Compute the sleep score based on the sleep data and recommendation data
    result = 0
    total = 0
    for _, row in reco_age.iterrows():
        indicator = row["indicator"]
        indicator_score = indicators[indicator]
        print(f"Computing score for indicator: {indicator} with value {indicator_score}")
        score, max_score = compute_score_for_row(row, indicator_score)
        print(f"Score for indicator {indicator}: {score}")
        result += score
        total += max_score
    return result / total * 100 if total > 0 else 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Compute the sleep score based on the provided sleep data CSV file."
    )
    parser.add_argument(
        "sleep_csv",
        type=str,
        help="Path to the sleep data CSV file.",
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

    # Load age
    age = args.age
    
    # Load the age file
    age_data = pd.read_csv(args.age_csv)

    # Load the sleep recommendation file
    recommendation_data = pd.read_csv(args.recommendation_csv)

    # Load the sleep data from a CSV file
    # sleep_data = pd.read_csv(args.sleep_csv)
    # Trouve la première ligne vide (séparateur header / tableau)
    with open(args.sleep_csv, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    sep_idx = next(i for i, l in enumerate(lines) if l.strip() == "")

    # Le tableau commence juste après
    sleep_data = pd.read_csv(args.sleep_csv, skiprows=sep_idx + 1)

    # Extract the category of age of the subject from the age data
    age_category = extract_category(age, age_data)
    print(f"Age category: {age_category}")

    # Extract the recommendation based on the age category
    reco_age = recommendation_data[recommendation_data["age_category"] == age_category]
    print(f"Recommendation based on age category: {reco_age}")

    # Calculate the sleep score based on the provided data
    indicators = computes_indicators(sleep_data, reco_age)
    print(f"Indicators score: {indicators}")

    # Compute the sleep score based on the indicators score
    print(f"recommendation for age: {reco_age}")
    sleep_score = compute_sleep_score(reco_age, indicators)

    # Print the sleep score
    print(f"Your sleep score is: {sleep_score}")