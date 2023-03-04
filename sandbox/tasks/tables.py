import django_tables2 as tables
from tasks.models import Task


class TaskTable(tables.Table):
    date_added = tables.DateColumn(format="M d, Y")
    date_completed = tables.DateColumn(format="M d, Y")

    class Meta:
        model = Task
        fields = (
            "name",
            "date_added",
        )
