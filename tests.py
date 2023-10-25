import pytest

from books_collector import BooksCollector

@pytest.mark.parametrize(
    ('book_name', 'expected_books_genre'),
    (
            ('', {}),
            (''.join(['s' for _ in range(41)]), {}),
            ('correct_book', {'correct_book': ''}),
    )
)
def test_add_new_book(book_name: str, expected_books_genre: {}):
    collector = BooksCollector()
    collector.add_new_book(book_name)
    assert collector.get_books_genre() == expected_books_genre


def test_add_new_book_existing_name_add_one():
    collector = BooksCollector()
    book_name = 'Some book'

    collector.add_new_book(book_name)
    collector.add_new_book(book_name)

    assert collector.get_books_genre() == {book_name: ''}


@pytest.mark.parametrize(
    ('genre', 'expected_book_genre'),
    (
            ('Фантастика', 'Фантастика'),
            ('Ужасы', 'Ужасы'),
            ('Детективы', 'Детективы'),
            ('Мультфильмы', 'Мультфильмы'),
            ('Комедии', 'Комедии'),
            ('Несуществующий жанр', ''),
    )
)
def test_set_book_genre(genre: str, expected_book_genre: str):
    collector = BooksCollector()
    book_name = 'Some book'

    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)

    assert collector.get_books_genre() == {book_name: expected_book_genre}


def test_set_book_genre_non_existent_book_pass():
    collector = BooksCollector()
    collector.set_book_genre('Some book', 'Мультфильмы')

    assert collector.get_books_genre() == {}


def test_get_book_genre_non_existent_book_none():
    collector = BooksCollector()
    book_genre = collector.get_book_genre('Non existent book')

    assert book_genre is None


def test_get_book_genre_exiting_book_none():
    collector = BooksCollector()
    book_name = 'Some book'
    genre = 'Комедии'

    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)
    book_genre = collector.get_book_genre(book_name)

    assert book_genre == genre


@pytest.mark.parametrize(
    ('books_genre', 'specific_genre', 'expected_books'),
    (
            ({}, 'Несуществующий жанр', []),
            ({}, 'Комедии', []),
            ({'Book1': 'Фантастика', 'Book2': 'Фантастика'}, 'Несуществующий жанр', []),
            ({'Book1': 'Фантастика', 'Book2': 'Фантастика'}, 'Комедии', []),
            ({'Book1': 'Фантастика', 'Book2': 'Фантастика'}, 'Фантастика', ['Book1', 'Book2']),
            ({'Book1': 'Фантастика', 'Book2': 'Фантастика', 'Book3': 'Детективы'}, 'Фантастика', ['Book1', 'Book2']),
    )
)
def test_get_books_with_specific_genre(books_genre: dict, specific_genre: str, expected_books: list):
    collector = BooksCollector()

    collector.books_genre = books_genre
    books_with_specific_genre = collector.get_books_with_specific_genre(specific_genre)

    assert books_with_specific_genre == expected_books


@pytest.mark.parametrize(
    ('books_genre', 'expected_books_genre'),
    (
            ({}, {}),
            ({'Book1': '', 'Book2': ''}, {'Book1': '', 'Book2': ''}),
            ({'Book1': 'Фантастика', 'Book2': 'Детективы'}, {'Book1': 'Фантастика', 'Book2': 'Детективы'})
    )
)
def test_get_books_genre(books_genre: dict, expected_books_genre: dict):
    collector = BooksCollector()
    collector.books_genre = books_genre

    assert collector.get_books_genre() == expected_books_genre


@pytest.mark.parametrize(
    ('books_genre', 'expected_books'),
    (
            ({}, []),
            ({'Book1': 'Фантастика', 'Book2': 'Мультфильмы', 'Book3': 'Комедии'}, ['Book1', 'Book2', 'Book3']),
            ({'Book1': 'Ужасы', 'Book2': 'Детективы'}, []),
            (
                    {
                        'Book1': 'Фантастика',
                        'Book2': 'Ужасы',
                        'Book3': 'Детективы',
                        'Book4': 'Мультфильмы',
                        'Book5': 'Комедии'
                    },
                    ['Book1', 'Book4', 'Book5']
            )
    )
)
def test_get_books_for_children(books_genre: dict, expected_books: list):
    collector = BooksCollector()
    collector.books_genre = books_genre

    assert collector.get_books_for_children() == expected_books


def test_add_book_in_favorites_non_existent_book_empty_list():
    collector = BooksCollector()
    collector.books_genre = {
        'Book1': 'Фантастика',
        'Book2': 'Ужасы',
        'Book3': 'Детективы',
        'Book4': 'Мультфильмы',
        'Book5': 'Комедии'
    }

    collector.add_book_in_favorites('Book100')

    assert collector.get_list_of_favorites_books() == []


def test_add_book_in_favorites_new_book_one_book():
    collector = BooksCollector()
    collector.books_genre = {
        'Book1': 'Фантастика',
        'Book2': 'Ужасы',
        'Book3': 'Детективы',
        'Book4': 'Мультфильмы',
        'Book5': 'Комедии'
    }

    collector.add_book_in_favorites('Book4')

    assert collector.get_list_of_favorites_books() == ['Book4']


def test_add_book_in_favorites_existing_book_one_book():
    collector = BooksCollector()
    collector.books_genre = {
        'Book1': 'Фантастика',
        'Book2': 'Ужасы',
        'Book3': 'Детективы',
        'Book4': 'Мультфильмы',
        'Book5': 'Комедии'
    }

    collector.add_book_in_favorites('Book1')
    collector.add_book_in_favorites('Book1')

    assert collector.get_list_of_favorites_books() == ['Book1']


def test_delete_book_from_favorites_non_existent_book_empty_list():
    collector = BooksCollector()
    collector.delete_book_from_favorites('Book1')

    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_existing_book_empty_list():
    collector = BooksCollector()
    collector.favorites = ['Book1']

    collector.delete_book_from_favorites('Book1')

    assert collector.get_list_of_favorites_books() == []


def test_get_list_of_favorites_books_empty_list():
    collector = BooksCollector()
    assert collector.get_list_of_favorites_books() == []


def test_get_list_of_favorites_books_list():
    collector = BooksCollector()
    collector.books_genre = {
        'Book1': 'Фантастика',
        'Book2': 'Ужасы',
        'Book3': 'Детективы',
        'Book4': 'Мультфильмы',
        'Book5': 'Комедии'
    }

    collector.add_book_in_favorites('Book1')
    collector.add_book_in_favorites('Book3')
    collector.add_book_in_favorites('Book5')

    collector.delete_book_from_favorites('Book3')

    assert collector.get_list_of_favorites_books() == ['Book1', 'Book5']