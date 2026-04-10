from interfaces import IRepository


class LibraryService:

    def __init__(self, repository: IRepository):
        self._repository = repository

    def import_data_from_file(self, file_path: str) -> None:
        raw_rows = self._repository.read_csv(file_path)
        total = len(raw_rows)
        print(f"[INFO] Зчитано рядків: {total}")

        for idx, row in enumerate(raw_rows, start=1):
            author_data = {
                'full_name': row['author_full_name'],
                'nationality': row['author_nationality'],
                'birth_year': row['author_birth_year'],
                'email': row['author_email'],
            }
            book_data = {
                'title': row['book_title'],
                'genre': row['book_genre'],
                'price': row['price'],
                'copies_available': row['copies_available'],
            }
            self._repository.save_author_with_book(author_data, book_data)

            if idx % 100 == 0 or idx == total:
                print(f"[INFO] Збережено {idx}/{total} записів...")

        print("[INFO] Імпорт завершено успішно.")

    def get_books(self):
        return self._repository.get_all_books()

    def get_authors(self):
        return self._repository.get_all_authors()

    def get_affordable_books(self, max_price: float):
        return [b for b in self._repository.get_all_books() if b.price <= max_price]
