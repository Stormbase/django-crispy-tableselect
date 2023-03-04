from django_tables2 import SingleTableView
from tasks.models import Task
from tasks.tables import TaskTable


class TaskTableView(SingleTableView):
    model = Task
    table_class = TaskTable
    template_name = "task_table_page.html"

    def get_queryset(self):
        return super().get_queryset().filter(date_completed__isnull=True)
