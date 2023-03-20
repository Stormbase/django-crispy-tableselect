from crispy_forms import layout
from crispy_forms.utils import TEMPLATE_PACK
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django_tables2 import Table

from .columns import CheckBoxColumn
from .helpers import TableSelectHelper


class TableSelect(layout.TemplateNameMixin):
    template = "django_tableselect/table_select.html"

    def __init__(
        self,
        name,
        table_class,
        table_data=[],
        table_kwargs={},
        helper=TableSelectHelper(),
        **kwargs,
    ):
        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

        self.name = name
        self.helper = helper
        self.table_class = table_class
        self.table_data = table_data
        self.table_kwargs = table_kwargs

    def _set_row_value(self, row, key, value):
        """Sets a value on the row, supports dicts and objects."""
        if isinstance(row, dict):
            row[key] = value
            return

        if isinstance(row, object):
            setattr(row, key, value)

    def prepare_table_data(self, table_data, values):
        """Prepare table data with values necessary for the select checkbox."""

        for row in table_data:
            value = self.helper.get_value(row)

            # Set the value of the checkbox
            self._set_row_value(row, self.name, value)

            # Set the checked state of the checkbox
            selected = str(value) in values
            self._set_row_value(row, "_selected", selected)
        return table_data

    def _construct_sequence(self, column_name):
        table_kwargs = self.table_kwargs.copy()
        kwarg_sequence = table_kwargs.pop("sequence", ())
        meta_sequence = ()
        if hasattr(self.table_class, "Meta") and hasattr(
            self.table_class.Meta, "sequence"
        ):
            meta_sequence = getattr(self.table_class.Meta, "sequence")

        original_sequence = kwarg_sequence or meta_sequence

        # Reconstruct the sequence with the checkbox column at the start
        return (column_name, *original_sequence)

    def get_table(self, input_name, values):
        column_name = self.name
        table_kwargs = self.table_kwargs.copy()

        extra_columns = [
            (
                column_name,
                CheckBoxColumn(
                    verbose_name="",
                    checked=lambda _, r: r.get("_selected"),
                    input_name=input_name,
                    helper=self.helper,
                ),
            )
        ]
        extra_columns.extend(table_kwargs.pop("extra_columns", []))
        sequence = self._construct_sequence(column_name)

        return self.table_class(
            # This table may never be ordered
            orderable=False,
            data=self.prepare_table_data(self.table_data, values),
            sequence=sequence,
            extra_columns=extra_columns,
            **table_kwargs,
        )

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        bound_field = form[self.name]
        values = bound_field.field.widget.format_value(bound_field.value())
        html_name = bound_field.html_name
        context.update({"table": self.get_table(html_name, values)})
        return render_to_string(template, context.flatten())
