import pytest

from django_crispy_tableselect import TableSelectHelper

from .testapp import factories, models, tables


@pytest.fixture
def book_factory():
    return factories.BookFactory


@pytest.fixture
def author_factory():
    return factories.AuthorFactory


@pytest.fixture
def books_tableselect(book_factory):
    def inner_func(**extra_args):
        qs = models.Book.objects.none()
        if "table_data" not in extra_args:
            book_factory.create_batch(10)
            qs = models.Book.objects.all()

        kwargs = {
            "column_name": "selected_books",
            "table_class": tables.BookTable,
            "table_data": extra_args.pop("table_data", qs),
            "label_field": "title",
            **extra_args,
        }
        return TableSelectHelper(**kwargs)

    return inner_func
