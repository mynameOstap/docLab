from infrastructure import SqliteRepository
from business_logic import LibraryService
from presentation import ConsolePresentationLayer


def main():
    repository = SqliteRepository(db_url="sqlite:///library.db")

    service = LibraryService(repository=repository)

    ui = ConsolePresentationLayer()

    import os
    if not os.path.exists("data.csv"):
        print("[INFO] data.csv не знайдено — генеруємо автоматично...")
        from generate_csv import generate_csv
        generate_csv("data.csv", rows=1050)

    service.import_data_from_file("data.csv")

    books = service.get_books()
    authors = service.get_authors()

    print("\n── Перші 10 книг ──")
    ui.display_books(books[:10])

    print("\n── Всі автори ──")
    ui.display_authors(authors)

    print("\n── Книги до 300 грн ──")
    affordable = service.get_affordable_books(max_price=300.0)
    ui.display_books(affordable[:10])
    print(f"(показано 10 з {len(affordable)} доступних за ціною книг)")


if __name__ == "__main__":
    main()
