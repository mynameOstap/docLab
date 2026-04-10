from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    def read_csv(self, file_path: str):
        pass

    @abstractmethod
    def save_author_with_book(self, author_dict: dict, book_dict: dict):
        pass

    @abstractmethod
    def get_all_books(self):
        pass

    @abstractmethod
    def get_all_authors(self):
        pass


class IPresentationLayer(ABC):

    @abstractmethod
    def display_books(self, books):
        pass

    @abstractmethod
    def display_authors(self, authors):
        pass
