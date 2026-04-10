from interfaces import IPresentationLayer


class ConsolePresentationLayer(IPresentationLayer):

    def display_books(self, books) -> None:
        print(f"\n{'='*75}")
        print(f"{'ID':<5} {'Назва':<35} {'Жанр':<18} {'Ціна':>8} {'Примірники':>10}")
        print(f"{'-'*75}")
        for b in books:
            print(f"{b.id:<5} {b.title:<35} {b.genre:<18} {b.price:>8.2f} {b.copies_available:>10}")
        print(f"{'='*75}\nВсього книг: {len(books)}\n")

    def display_authors(self, authors) -> None:
        print(f"\n{'='*75}")
        print(f"{'ID':<5} {'ПІБ':<30} {'Email':<30} {'Нац.':<12} {'Рік':>5}")
        print(f"{'-'*75}")
        for a in authors:
            print(f"{a.id:<5} {a.full_name:<30} {a.email:<30} {a.nationality:<12} {a.birth_year:>5}")
        print(f"{'='*75}\nВсього авторів: {len(authors)}\n")
