from django_tables2 import SingleTableView
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormView
from tasks.models import Task
from tasks.tables import TaskTable
from tasks.forms import BulkCompleteTaskForm


class TaskTableView(SingleTableView):
    model = Task
    table_class = TaskTable
    template_name = "task_table_page.html"

class BulkCompleteTaskView(MultipleObjectMixin, FormView):
    form_class = BulkCompleteTaskForm
    model = Task
    template_name = "task_bulk_complete_page.html"
    success_url = reverse_lazy("tasks:bulk-complete")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tasks"] = self.get_queryset()

        return kwargs

    def form_valid(self, form):
        task_ids = form.cleaned_data.get('select_tasks')
        date_completed = form.cleaned_data.get('date_completed')

        Task.objects.filter(id__in=task_ids).update(date_completed=date_completed)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().dispatch(request, *args, **kwargs)
