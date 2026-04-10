import csv
import random
import sys

GENRES = [
    "Фантастика", "Детектив", "Романтика", "Жахи", "Пригоди",
    "Наукова фантастика", "Біографія", "Історичний роман", "Поезія", "Психологія"
]

NATIONALITIES = ["Українська", "Польська", "Американська", "Британська", "Французька", "Німецька", "Японська"]

BOOK_TEMPLATES = [
    "Таємниця {}",
    "Останній {}",
    "Зоряний {}",
    "Пригоди {}",
    "Тінь {}",
    "Серце {}",
    "Код {}",
    "Вогонь {}",
    "Голос {}",
    "Місто {}",
    "Легенда про {}",
    "Повернення {}",
    "Забутий {}",
    "Нічний {}",
    "Крила {}",
    "Острів {}",
    "Межа {}",
    "Дзеркало {}",
    "Сон {}",
    "Рівновага {}",
]

AUTHOR_FIRST_NAMES = ["Олег", "Марія", "Іван", "Анна", "Петро", "Олена", "Василь", "Тетяна", "Андрій", "Наталія"]
AUTHOR_LAST_NAMES = ["Коваленко", "Шевченко", "Бондаренко", "Мельник", "Лисенко", "Поліщук", "Ткаченко", "Кравченко", "Гончаренко", "Савченко"]


def generate_csv(filename: str = "data.csv", rows: int = 1050) -> None:
    if rows < 1000:
        print("[WARN] Мінімальна кількість рядків — 1000. Встановлено 1000.")
        rows = 1000

    num_authors = min(50, rows)
    authors = []
    used_emails = set()
    for i in range(num_authors):
        first = AUTHOR_FIRST_NAMES[i % len(AUTHOR_FIRST_NAMES)]
        last = AUTHOR_LAST_NAMES[i % len(AUTHOR_LAST_NAMES)]
        email = f"author{i}@library.ua"
        if email in used_emails:
            email = f"author{i}_alt@library.ua"
        used_emails.add(email)
        authors.append({
            'full_name': f"{last} {first}",
            'nationality': random.choice(NATIONALITIES),
            'birth_year': random.randint(1940, 1995),
            'email': email,
        })

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "book_title", "book_genre", "price", "copies_available",
            "author_full_name", "author_nationality", "author_birth_year", "author_email"
        ])

        for i in range(rows):
            author = authors[i % num_authors]
            template = BOOK_TEMPLATES[i % len(BOOK_TEMPLATES)]
            writer.writerow([
                template.format(i + 1),
                random.choice(GENRES),
                round(random.uniform(50.0, 1200.0), 2),
                random.randint(0, 500),
                author['full_name'],
                author['nationality'],
                author['birth_year'],
                author['email'],
            ])

    print(f"[OK] Файл «{filename}» згенеровано: {rows} рядків даних.")


if __name__ == "__main__":
    _rows = int(sys.argv[1]) if len(sys.argv) > 1 else 1050
    _file = sys.argv[2] if len(sys.argv) > 2 else "data.csv"
    generate_csv(_file, _rows)
