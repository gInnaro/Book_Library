import uuid
import json
import os

class Book:
    def __init__(self, title, author, year, status="в наличии", book_id=None):
        """Инициализация книги
        Добавление таких характеристик для книги, как:
        - id (уникальный идентификатор, генерируется автоматически)
        - title (название книги)
        - author (автор книги)
        - year (год издания)
        - status (статус книги: “в наличии”, “выдана”)"""
        self.id = book_id if book_id else str(uuid.uuid4()) #Генерация уникального индентификатора
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"ID: {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод: {self.year}\nСтатус: {self.status}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["year"], data["status"], data["id"])

class Library:
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = self.load_books()

    def add_book(self, title, author, year, status="в наличии"):
        """Добавление новой книги в библиотеку"""
        book = Book(title, author, year, status)
        self.books.append(book)
        self.save_books()
        print("Книга добавлена успешно!")

    def delete_book(self, book_id):
        """Удаление книги из библиотеки"""
        if any(book.id == book_id for book in self.books): #Проверка на существование книги с таким Айди
            self.books = [book for book in self.books if book.id != book_id] #Создание списка без книги
            self.save_books()
            print("Книга удалена успешно!")
        else:
            print("Книга с таким ID не найдена.")

    def find_book(self, search_term):
        """Поиск книги по названию, или по автору, или году выпуска"""
        results = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower() or search_term.lower() in book.year.lower()]
        return results

    def display_books(self):
        """Отобразить все книги"""
        if not self.books:
            print("Библиотека пуста.")
        else:
            for book in self.books:
                print(f"\n{book}")

    def change_book_status(self, book_id, new_status):
        """Обновление статуса книги"""
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print("Статус книги обновлен успешно!")
                return
        print("Книга с таким ID не найдена.")

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return [Book.from_dict(data) for data in json.load(f)]
        return []

def main():
    library = Library()

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = input("Введите ID книги для удаления: ")
            library.delete_book(book_id)

        elif choice == '3':
            search_term = input("Введите название или автора книги или год издания для поиска: ")
            results = library.find_book(search_term)
            if results:
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = input("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус книги (в наличии/выдана): ")
            if new_status.lower() in ("в наличии", "выдана"):
                library.change_book_status(book_id, new_status.lower())
            else:
                print("Неверный статус")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()