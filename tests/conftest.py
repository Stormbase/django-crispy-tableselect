import pytest

from django_crispy_tableselect import TableSelectHelper
from sandbox import factories, models, tables


@pytest.fixture
def book_factory():
    return factories.BookFactory


@pytest.fixture
def author_factory():
    return factories.AuthorFactory


@pytest.fixture
def books_tableselecthelper(book_factory):
    """Return an instance of TableSelectHelper that is operating on a collection of 10 books.

    Accepts an `table_data` argument to pass your own data.
    All other kwargs are passed as-is to TableSelectHelper.__init__()
    """

    def inner_func(**extra_args):
        qs = models.Book.objects.none()
        if "table_data" not in extra_args:
            book_factory.create_batch(10)
            qs = models.Book.objects.all()

        kwargs = {
            "column_name": "selected_books",
            "table_class": tables.BookTable,
            "table_data": extra_args.pop("table_data", qs),
            "label": "title",
            **extra_args,
        }
        return TableSelectHelper(**kwargs)

    return inner_func
