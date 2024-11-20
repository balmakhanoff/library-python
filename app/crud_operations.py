from .utils import json_library_reader, logger, append_to_json_library
import datetime

current_year: datetime = datetime.datetime.now().year


class Operations:
    """Operations class provides methods to manage a library system. 
       It includes functionality to add, delete, view, search books, and change the status of a book."""

    @staticmethod
    def add_book() -> None:
        """Adds a new book to the library. The user provides the title, author, year, and status of the book."""
        book: dict = {}
        params: list = ['title', 'author', 'year', 'status']
        books: list = json_library_reader()
        max_id: int = max([book['id'] for book in books], default=0)
        book['id'] = max_id + 1

        try:
            for param in params:
                while True:
                    book[param] = input(f"Enter please {param}: ").lower()

                    if param == 'author':
                        if any(char.isdigit() for char in book[param]):
                            print("Author name cannot contain numbers.")
                            continue

                    if param == 'year':
                        if not book[param].isdigit() or len(book[param]) != 4:
                            print("Year must be a 4-digit number.")
                            continue

                        year = int(book[param])
                        if year > current_year:
                            print(
                                f"Year cannot be greater than the current year ({current_year}).")
                            continue

                    if param == 'status':
                        if book[param] not in ('в наличии', 'выдана'):
                            print('The anser should be "в наличии" or "выдана"')
                            continue

                    if book[param] != '':
                        break

            books.append(book)
            append_to_json_library(books)
            logger(f'Added {book}', 'info')
            print(f'Book Succesfully added ID is {book['id']}\n')
        except Exception as err:
            logger(err, 'error')

    @staticmethod
    def delete_book() -> None:
        """Deletes a book from the library by its ID."""

        books: list = json_library_reader()
        try:
            while True:
                choice: str = input(
                    'Which book do you prefer to delete? Enter ID: ')
                if not choice.isdigit():
                    print('You should type only numbers')
                    continue

                book_exists: bool = any(
                    book['id'] == int(choice) for book in books)
                if not book_exists:
                    print(f"Book with ID {choice} does not exist.")
                    continue

                break

            updated_book_list = [
                book for book in books if book['id'] != int(choice)]
            append_to_json_library(updated_book_list)
            print(f'ID {choice} successfuly deleted\n')
            logger(f'ID {choice} successfuly deleted', 'info')
        except Exception as err:
            logger(err, 'error')

    @staticmethod
    def show_books(custom_books: list = []) -> None:
        """Displays all books in the library or a custom list of books."""

        books: list = json_library_reader()
        if custom_books:
            books: list = custom_books
        print('ALL BOOKS')
        try:
            for i, book in enumerate(books):
                print(f'# {i}')
                print(f' - Id: {book['id']}')
                print(f' - Title: {book['title'].title()}')
                print(f' - Author: {book['author'].title()}')
                print(f' - Year: {book['year']}')
                print(f' - Status: {book['status'].capitalize()}\n')

            logger('Books have been showed', 'info')
        except Exception as err:
            logger(err, 'error')

    @staticmethod
    def search_the_book() -> None:
        """Searches for books by title, author, or year."""

        try:
            search_input = input(
                'You can search in title, author or year: ').strip().lower()
            books = json_library_reader()

            if not books:
                print("No books found in the library.")
                return

            matching_books = [
                book for book in books if (
                    search_input in book['title'] or
                    search_input in book['author'] or
                    search_input in str(book['year']))]

            data_length = len(matching_books)

            if data_length < 1:
                print('No match')
                return

            Operations.show_books(matching_books)
            print(f'Found {data_length} books\n')
        except Exception as err:
            logger(err, 'error')

    @staticmethod
    def change_book_status():
        """Updates the status of a book by its ID."""

        books: list = json_library_reader()

        if not books:
            print("No books found in the library.")
            return

        try:
            while True:
                book_id_input: str = input(
                    "Which book status do you wanna change? Enter ID: ").strip()

                if not book_id_input.isdigit():
                    print("Invalid ID. Please enter a numeric ID.")
                    return

                book_id_input = int(book_id_input)
                book_exists: bool = False

                for book in books:
                    if book['id'] == book_id_input:
                        book_exists = True
                        break

                if not book_exists:
                    print(f"Book with ID {book_id_input} not found.\n")
                    return

                status: str = input(
                    'Enter new status (в наличии / выдана): ').lower().strip()

                if status not in ['в наличии', 'выдана']:
                    print('The answer should be "в наличии" or "выдана".')
                    continue

                for book in books:
                    if book['id'] == book_id_input:
                        book['status'] = status
                        break

                append_to_json_library(books)

                print(f'Book with ID {
                      book_id_input} status has been updated to {status}.')
                logger(
                    'Book with ID {book_id_input} status has been updated to {status}.', 'info')
                break
        except Exception as err:
            logger(err, 'error')
