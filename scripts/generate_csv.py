import csv
import os
import random

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "insurance_products.csv")

PRODUCT_NAMES = [
    "Allianz Travel Basic",
    "Allianz Travel Plus",
    "Allianz Travel Premium",
    "Allianz Health Guard",
    "Allianz Emergency Assist",
    "Allianz Explorer Shield",
    "Allianz Global Care",
    "Allianz Tropical Cover",
    "Allianz Adventure Pack",
    "Allianz Medical Evacuation",
]

COVERAGE_TYPES = [
    "Медичне страхування",
    "Страхування від нещасних випадків",
    "Евакуація та репатріація",
    "Страхування багажу",
    "Відміна подорожі",
    "Комплексне покриття",
]

HIGH_RISK_COUNTRIES = [
    "Індія", "Бразилія", "Нігерія", "Конго", "Таїланд",
    "В'єтнам", "Індонезія", "Кенія", "Колумбія", "Перу",
    "Єгипет", "Камбоджа", "Мадагаскар", "Болівія", "Танзанія",
]

RISK_LEVELS = ["Низький", "Середній", "Високий", "Критичний"]
AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]

HEALTH_CONDITIONS = [
    "Здоровий", "Хронічні захворювання", "Алергії",
    "Серцево-судинні", "Діабет",
]

DURATIONS = ["7 днів", "14 днів", "21 день", "30 днів", "60 днів", "90 днів"]


def generate_records(count: int = 50) -> list:
    records = []

    for i in range(count):
        country = random.choice(HIGH_RISK_COUNTRIES)

        if country in ["Конго", "Нігерія", "Мадагаскар"]:
            risk = random.choice(["Високий", "Критичний"])
        elif country in ["Індія", "Бразилія", "Кенія", "Танзанія"]:
            risk = random.choice(["Середній", "Високий"])
        else:
            risk = random.choice(RISK_LEVELS)

        base_premium = {
            "Низький": random.uniform(30, 80),
            "Середній": random.uniform(80, 200),
            "Високий": random.uniform(200, 500),
            "Критичний": random.uniform(500, 1200),
        }[risk]

        age_group = random.choice(AGE_GROUPS)
        age_multiplier = {
            "18-25": 0.9, "26-35": 1.0, "36-45": 1.15,
            "46-55": 1.35, "56-65": 1.6, "65+": 2.0,
        }[age_group]

        health = random.choice(HEALTH_CONDITIONS)
        health_multiplier = {
            "Здоровий": 1.0, "Хронічні захворювання": 1.5,
            "Алергії": 1.1, "Серцево-судинні": 1.7, "Діабет": 1.4,
        }[health]

        premium = round(base_premium * age_multiplier * health_multiplier, 2)

        record = {
            "product_id": f"ALZ-{1000 + i}",
            "product_name": random.choice(PRODUCT_NAMES),
            "coverage_type": random.choice(COVERAGE_TYPES),
            "destination_country": country,
            "risk_level": risk,
            "age_group": age_group,
            "health_condition": health,
            "duration": random.choice(DURATIONS),
            "premium_eur": str(premium),
            "max_coverage_eur": str(random.choice([10000, 25000, 50000, 100000, 250000])),
            "deductible_eur": str(random.choice([0, 50, 100, 200, 500])),
        }
        records.append(record)

    return records


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    records = generate_records(50)

    fieldnames = [
        "product_id", "product_name", "coverage_type",
        "destination_country", "risk_level", "age_group",
        "health_condition", "duration", "premium_eur",
        "max_coverage_eur", "deductible_eur",
    ]

    with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Згенеровано {len(records)} записів у {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
