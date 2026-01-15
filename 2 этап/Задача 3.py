# Система управления библиотекой книг
import json
PATH = r'library.json'
class Book: # Класс Книга
    def __init__(self, title: str, isbn: str, author: str, genre: str, year: int):
        if not isbn.isdigit():
            raise ValueError("ISBN должен состоять только из цифр")
        self.title = title
        self.isbn = isbn
        self.author = author
        self.genre = genre
        self.year = year
        self.issued = False
        self.reader = None

    def __str__(self):
        if self.issued:
            status = 'выдана'
        else:
            status = 'доступна'
        if self.reader:
            reader_name = f', читатель: {self.reader}'
        else:
            reader_name = ''
        return (f'Книга: {self.title}\n'
                f'Автор: {self.author}\n'
                f'Жанр: {self.genre}\n'
                f'ISBN: {self.isbn}\n'
                f'Статус: {status} {reader_name}')

    def issue_book(self, reader_name): # Меняет статус выдачи книги
        if self.issued:
            raise ValueError("Книга уже выдана")
        self.issued = True
        self.reader_name = reader_name
    def return_book(self): # Меняет статус выдачи книги
        if not self.issued:
            raise ValueError("Книга не была выдана")
        self.issued = False
        self.reader = None
    def to_json(self): # Сериализация
        return {"title": self.title, "isbn": self.isbn, "author": self.author,
            "genre": self.genre, "year": self.year, "issued": self.issued,
            "reader": self.reader}

    @classmethod
    def from_json(cls, data: dict): # Десериализация
        book = cls(data["title"],data["isbn"], data["author"], data["genre"],
            data["year"])
        book.issued = data["issued"]
        book.reader = data["reader"]
        return book


class LibraryManager: #  Система управления книгами
    def __init__(self):
        self.library = self._load()

    def __str__(self):
        return '\n\n'.join(str(book) for book in self.library.values())
    def _save(self):
        data = {isbn: book.to_json() for isbn, book in self.library.items()}

        with open(PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    def _load(self):
        try:
            with open(PATH, "r", encoding="utf-8") as f:
                if f.read().strip() == "":
                    return {}
                f.seek(0)
                data = json.load(f)

            return {isbn: Book.from_json(value) for isbn, value in data.items()}

        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    def add_book(self, book): #  Добавить книгу
        if book.isbn in self.library:
            raise ValueError("Книга с таким ISBN уже существует")

        self.library[book.isbn] = book
        self._save()
    def remove_book(self, isbn): #  Удалить книгу
        if isbn not in self.library:
            raise KeyError("Книга не найдена")

        del self.library[isbn]
        self._save()
    def issue_book(self, isbn, reader_name): #  Выдать книгу
        self._get(isbn).issue_book(reader_name)
        self._save()
    def return_book(self, isbn): #  Вернуть книгу
            self._get(isbn).return_book()
            self._save()
    def _get(self, isbn): #  Вспомогатеьльная функция вызова объект книги
        if isbn not in self.library:
            raise KeyError("Книга не найдена")
        return self.library[isbn]
    def get_statistics(self):
        by_genre = {}
        by_year = {}
        for book in self.library.values():
            by_genre[book.genre] = by_genre.get(book.genre, 0) + 1
            by_year[book.year] = by_year.get(book.year, 0) + 1
        return {"genres": by_genre,"years": by_year}



library = LibraryManager()

library.add_book(Book("Приключения Тома Сойера", "9780143039563", "Марк Твен", "Приключения", 1876))
library.add_book(Book("Янки из Коннектикута при дворе короля Артура", "9780140430646", "Марк Твен", "Фантастика", 1889))
library.add_book(Book("The Hobbit", "9780547928227", "J.R.R. Tolkien", "Фэнтези", 1937))
library.add_book(Book("Чистый код", "9780547928349", "Роберт Мартин", "IT", 2008))
library.add_book(Book("Python Crash Course", "9780547928751", "Эрик Маттес", "IT", 2019))

library.issue_book("9780140430646", "Владлен ")
library.return_book("9780140430646")

print(library)
print(library.get_statistics())