import django_tables2 as tables

from sandbox.models import Book, Task


class TaskTable(tables.Table):
    date_added = tables.DateColumn(format="M d, Y")
    date_completed = tables.DateColumn(format="M d, Y")

    class Meta:
        model = Task
        fields = (
            "name",
            "date_added",
        )
        attrs = {
            "class": "my-table",
        }


class BookTable(tables.Table):
    class Meta:
        model = Book
        fields = ("title", "author", "date_published")
