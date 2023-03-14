from django import forms
from django.core.exceptions import ValidationError
import datetime

from django_tables2.columns import BooleanColumn
from techonomy.django.django_tableselect import TableSelectMultipleWidget


from .tables import TaskTable

class BulkCompleteTaskForm(forms.Form):
    date_completed = forms.DateField(
        required=True,
        initial=datetime.date.today(),
        # help_text="Must be a date in the future",
        widget=forms.widgets.SelectDateWidget()
    )
    select_tasks = forms.fields.MultipleChoiceField(required=True, widget=TableSelectMultipleWidget)

    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["select_tasks"].choices = self.get_task_choices(tasks)
        self.fields["select_tasks"].widget.table_class = TaskTable
        # self.fields["select_tasks"].widget.table_kwargs = {
        #     # To test that the widget respects these django_tables2.Table keyword arguments
        #     "sequence": ("name", "...", "extra"),
        #     "extra_columns": [("extra", BooleanColumn(verbose_name="Extra"))]
        # }
        self.fields["select_tasks"].widget.data = tasks

    def clean_date_completed(self):
        date_completed = self.cleaned_data.get("date_completed")

        if date_completed < datetime.date.today():
            raise ValidationError("Date must be in the future")
        return date_completed

    def get_task_choices(self, tasks):
        return tasks.values_list("id", "name")