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
def test_add_new_book(book_name: str, expected_books_genre: dict):
    collector = BooksCollector()
    collector.add_new_book(book_name)
    assert collector.get_books_genre() == expected_books_genre


def test_add_new_book_existing_name_add_one():
    collector = BooksCollector()

    collector.add_new_book('Some book')
    collector.add_new_book('Some book')

    assert collector.get_books_genre() == {'Some book': ''}


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

    collector.add_new_book('Some book')
    collector.set_book_genre('Some book', genre)

    assert collector.get_books_genre() == {'Some book': expected_book_genre}


def test_set_book_genre_non_existent_book_pass():
    collector = BooksCollector()
    collector.set_book_genre('Some book', 'Мультфильмы')

    assert collector.get_books_genre() == {}


def test_get_book_genre_non_existent_book_none():
    collector = BooksCollector()
    assert collector.get_book_genre('Non existent book') is None


def test_get_book_genre_exiting_book_none():
    collector = BooksCollector()

    collector.add_new_book('Some book')
    collector.set_book_genre('Some book', 'Комедии')

    assert collector.get_book_genre('Some book') == 'Комедии'


def test_get_books_with_specific_genre():
    collector = BooksCollector()

    collector.add_new_book('Book1')
    collector.add_new_book('Book2')

    collector.set_book_genre('Book1', 'Фантастика')
    collector.set_book_genre('Book2', 'Детективы')

    assert collector.get_books_with_specific_genre('Детективы') == ['Book2']


def test_get_books_for_children():
    collector = BooksCollector()

    collector.add_new_book('Book1')
    collector.add_new_book('Book2')
    collector.add_new_book('Book3')
    collector.add_new_book('Book4')
    collector.add_new_book('Book5')
    collector.add_new_book('Book6')

    collector.set_book_genre('Book1', 'Фантастика')
    collector.set_book_genre('Book2', 'Ужасы')
    collector.set_book_genre('Book3', 'Детективы')
    collector.set_book_genre('Book4', 'Мультфильмы')
    collector.set_book_genre('Book5', 'Комедии')

    assert collector.get_books_for_children() == ['Book1', 'Book4', 'Book5']


def test_add_book_in_favorites_non_existent_book_empty_list():
    collector = BooksCollector()
    collector.add_book_in_favorites('Book100')
    assert collector.get_list_of_favorites_books() == []


def test_add_book_in_favorites_new_book_one_book():
    collector = BooksCollector()

    collector.add_new_book('Book4')
    collector.add_book_in_favorites('Book4')

    assert collector.get_list_of_favorites_books() == ['Book4']


def test_add_book_in_favorites_existing_book_one_book():
    collector = BooksCollector()

    collector.add_new_book('Book1')
    collector.add_book_in_favorites('Book1')
    collector.add_book_in_favorites('Book1')

    assert collector.get_list_of_favorites_books() == ['Book1']


def test_delete_book_from_favorites_non_existent_book_empty_list():
    collector = BooksCollector()
    collector.delete_book_from_favorites('Book1')

    assert collector.get_list_of_favorites_books() == []


def test_delete_book_from_favorites_existing_book_empty_list():
    collector = BooksCollector()

    collector.add_new_book('Book1')
    collector.add_book_in_favorites('Book1')
    collector.delete_book_from_favorites('Book1')

    assert collector.get_list_of_favorites_books() == []


def test_get_list_of_favorites_books_empty_list():
    collector = BooksCollector()
    assert collector.get_list_of_favorites_books() == []


def test_get_list_of_favorites_books_list():
    collector = BooksCollector()

    collector.add_new_book('Book1')
    collector.add_new_book('Book2')
    collector.add_new_book('Book3')

    collector.add_book_in_favorites('Book1')
    collector.add_book_in_favorites('Book3')

    assert collector.get_list_of_favorites_books() == ['Book1', 'Book3']
