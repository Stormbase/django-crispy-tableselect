import django_tables2 as tables

from .models import Book


class BookTable(tables.Table):
    class Meta:
        model = Book
        fields = ("title", "author", "date_published")
