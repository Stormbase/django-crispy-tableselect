from crispy_forms import layout
from crispy_forms.utils import TEMPLATE_PACK
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django_tables2 import Table

from .helpers import TableSelectHelper


class TableSelect(layout.TemplateNameMixin):
    template = "django_tableselect/table_select.html"

    def __init__(
        self,
        name,
        table_class,
        table_data=[],
        table_kwargs={},
        helper_class=TableSelectHelper,
        **kwargs,
    ):
        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

        self.name = name
        self.helper = helper_class(
            column_name=name,
            table_class=table_class,
            table_data=table_data,
            table_kwargs=table_kwargs
        )

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        bound_field = form[self.name]

        # Waarom hier niet gewoon bound_field.value()
        selected_values = bound_field.field.widget.format_value(bound_field.value())

        html_name = bound_field.html_name
        context.update({"table": self.helper.get_table(html_name, selected_values)})
        return render_to_string(template, context.flatten())
