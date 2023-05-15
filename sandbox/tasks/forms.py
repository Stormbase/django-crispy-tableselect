import datetime

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django_crispy_tableselect import TableSelect, TableSelectHelper, CrispyMediaMixin


from .tables import TaskTable


class BulkCompleteTaskForm(CrispyMediaMixin, forms.Form):
    date_completed = forms.DateField(
        required=True,
        initial=timezone.now(),
        help_text="Must be a date in the future",
        widget=forms.widgets.SelectDateWidget()
    )
    select_tasks = forms.fields.MultipleChoiceField(required=True)

    def __init__(self, tasks, *args, **kwargs):
        super().__init__(*args, **kwargs)

        table_helper = TableSelectHelper(
            column_name="select_tasks",
            table_class=TaskTable,
            table_data=tasks,
            allow_bulk_select=True,
        )
        self.fields["select_tasks"].choices = table_helper.choices

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("date_completed"),
            TableSelect("select_tasks", helper=table_helper),
            Submit("submit", "Submit")
        )

    def clean_date_completed(self):
        date_completed = self.cleaned_data.get("date_completed")

        if date_completed < datetime.date.today():
            raise ValidationError("Date must be in the future")
        return date_completed
