import pytest

from main import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    @pytest.mark.parametrize('name',
                             ['Что делать, если ваш кот хочет вас убить.',
                              'Что делать, если ваш кот хочет вас убить, а вы и не против',
                              '']
                             )
    def test_add_new_book_wrong_name_not_added(self, name):
        # проверка метода на добавление книги с длинным именем (41 символ или больше)
        collector = BooksCollector()

        collector.add_new_book(name)
        assert len(collector.get_books_genre()) == 0

    def test_add_new_book_existent_name_not_added(self):
        # проверка добавления уже имеемой книги
        collector = BooksCollector()

        collector.add_new_book('Чёрные дыры')
        collector.add_new_book('Чёрные дыры')
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize(
        'name, genre',
        [
            ['Малыш', 'Фантастика'],
            ['Утопленница', 'Ужасы'],
            ['Секрет', 'Детективы'],
            ['Путешествие Нильса', 'Мультфильмы'],
            ['Двенадцать стульев', 'Комедии']
        ]
    )
    def test_set_book_genre_allowed_genre_succeeds(self, name, genre):
        # позитивная проверка метода set_book_genre на все жанры из списка
        collector = BooksCollector()

        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    def test_set_book_genre_not_listed_not_set(self):
        # негативная проверка метода set_book_genre на жанр не из списка
        collector = BooksCollector()

        collector.add_new_book('Чёрные дыры')
        collector.set_book_genre('Чёрные дыры', 'Научпоп')
        assert collector.get_book_genre('Чёрные дыры') == ''

    def test_set_book_genre_name_not_present_not_set(self):
        # негативная проверка метода set_book_genre (и get_book_genre), если не найдено имя книги в словаре books_genre
        collector = BooksCollector()

        collector.set_book_genre('Малыш', 'Фантастика')
        assert collector.get_book_genre('Малыш') is None

    def test_get_books_with_specific_genre_two_books_found(self):
        # позитивная проверка метода get_books_with_specific_genre, если найдено более одной книги в жанре
        collector = BooksCollector()

        collector.add_new_book('Малыш')
        collector.add_new_book('Обитаемый остров')
        collector.add_new_book('Как ничего не понять и не подать виду')
        collector.set_book_genre('Малыш', 'Фантастика')
        collector.set_book_genre('Обитаемый остров', 'Фантастика')
        collector.set_book_genre('Как ничего не понять и не подать виду', 'Комедии')
        assert collector.get_books_with_specific_genre('Фантастика') == ['Малыш', 'Обитаемый остров']

    def test_get_books_with_specific_genre_empty_books_genre_not_found(self):
        # негативная проверка метода get_books_with_specific_genre, если словарь books_genre пустой
        collector = BooksCollector()

        assert len(collector.get_books_with_specific_genre('Фантастика')) == 0

    def test_get_books_with_specific_genre_not_genre_not_found(self):
        # негативная проверка метода get_books_with_specific_genre, если жанр для поиска указан неверно
        collector = BooksCollector()

        collector.add_new_book('Малыш')
        collector.set_book_genre('Малыш', 'Фантастика')
        assert len(collector.get_books_with_specific_genre('Комедии')) == 0

    def test_get_books_for_children_two_books_found(self):
        # позитивная проверка метода get_books_for_children - две книги из трёх найдено
        collector = BooksCollector()

        collector.add_new_book('Малыш')
        collector.set_book_genre('Малыш', 'Фантастика')
        collector.add_new_book('Обитаемый остров')
        collector.set_book_genre('Обитаемый остров', 'Фантастика')
        collector.add_new_book('Как ничего не понять и не подать виду')
        collector.set_book_genre('Морщерогие кизляки', 'Ужасы')
        assert collector.get_books_for_children() == ['Малыш', 'Обитаемый остров']

    def test_add_book_in_favorites_existent_book_added(self):
        # позитивная проверка добавления в Избранное
        collector = BooksCollector()

        collector.add_new_book('Малыш')
        collector.add_book_in_favorites('Малыш')
        assert 'Малыш' in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_not_favorite_book_not_removed(self):
        # проверка удаления из избранного, если книга не найдена в избранном
        collector = BooksCollector()

        collector.add_new_book('Малыш')
        collector.add_new_book('Обитаемый остров')
        collector.add_book_in_favorites('Малыш')
        collector.delete_book_from_favorites('Обитаемый остров')
        assert ['Малыш'] == collector.get_list_of_favorites_books()
