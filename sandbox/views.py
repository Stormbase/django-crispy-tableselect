from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.list import MultipleObjectMixin
from django_tables2 import SingleTableView
from formtools.wizard.views import SessionWizardView

from sandbox.forms import BulkCompleteTaskForm
from sandbox.models import Task
from sandbox.tables import TaskTable


class TaskTableView(SingleTableView):
    model = Task
    table_class = TaskTable
    template_name = "task_table_page.html"


class BulkCompleteTaskView(MultipleObjectMixin, SessionWizardView):
    form_list = [("tasks", BulkCompleteTaskForm)]
    model = Task
    template_name = "task_bulk_complete_page.html"
    success_url = reverse_lazy("tasks:bulk-complete")

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs()
        kwargs["tasks"] = self.get_queryset()

        return kwargs

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        task_ids = data.get("select_tasks")
        date_completed = data.get("date_completed")

        Task.objects.filter(id__in=task_ids).update(date_completed=date_completed)

        return HttpResponseRedirect(reverse_lazy("tasks:bulk-complete"))

    def dispatch(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().dispatch(request, *args, **kwargs)
