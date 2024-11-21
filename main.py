import json
import uuid
import os


class Book:
    def __init__(self, title, author, year):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    def __str__(self):
        return f"ID: {self.id}\nНазвание: {self.title}\nАвтор: {self.author}\nГод: {self.year}\nСтатус: {self.status}\n"

    def update_status(self, new_status):
        if new_status in ["в наличии", "выдана"]:
            self.status = new_status
        else:
            print("Неверный статус. Доступные статусы: 'в наличии', 'выдана'")


def load_books_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return [Book(book) for book in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
        return []


def save_books_to_file(filename, books):
    try:
        book_data = [book.__dict__ for book in books]
        with open(filename, 'w') as file:
            json.dump(book_data, file, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")


def add_book(books, filename):
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    try:
        year = int(input("Введите год издания: "))
    except ValueError:
        print("Некорректный год. Пожалуйста, введите число.")
        return
    new_book = Book(title, author, year)
    books.append(new_book)
    save_books_to_file(filename, books)


def delete_book(books, filename):
    book_id = input("Введите ID книги для удаления: ")
    for book in books[:]:  # Используем books[:] для копирования списка, избегая ошибки при изменении списка в цикле
        if book.id == book_id:
            books.remove(book)
            print("Книга удалена")
            save_books_to_file(filename, books)
            return
    print("Книга с указанным ID не найдена")


def search_book(books):
    search_term = input("Введите часть названия, автора или года для поиска: ")
    results = [
        book for book in books
        if search_term.lower() in book.title.lower()
           or search_term.lower() in book.author.lower()
           or str(book.year) == search_term
    ]
    if results:
        for book in results:
            print(book)
    else:
        print("Ничего не найдено")


def view_all_books(books):
    if not books:
        print("Список книг пуст.")
        return
    for book in books:
        print(book)


def update_book_status(books, filename):
    book_id = input("Введите ID книги: ")
    new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
    for book in books:
        if book.id == book_id:
            book.update_status(new_status)
            save_books_to_file(filename, books)
            print("Статус книги обновлен")
            return
    print("Книга с указанным ID не найдена")


if __name__ == "__main__":
    filename = "books.json"  # Имя файла для хранения данных
    books = load_books_from_file(filename)

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            add_book(books, filename)
        elif choice == '2':
            delete_book(books, filename)
        elif choice == '3':
            search_book(books)
        elif choice == '4':
            view_all_books(books)
        elif choice == '5':
            update_book_status(books, filename)
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
