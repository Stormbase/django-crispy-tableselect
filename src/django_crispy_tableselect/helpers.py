from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.forms.widgets import Media
from django.utils.translation import gettext_lazy as _
from django_tables2 import Table

from .columns import CheckBoxColumn


class TableSelectHelper:
    """Helper that houses various features related to TableSelect."""

    # Path to javascript static file
    js_path = "django_crispy_tableselect/tableselect.js"

    def __init__(
        self,
        column_name,
        table_class,
        table_data,
        label_field,
        value_field="id",
        *,
        table_kwargs={},
        allow_select_all=False,
    ):
        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

        self.column_name = column_name
        self.table_class = table_class
        self.table_data = table_data
        self.table_kwargs = table_kwargs
        self.allow_select_all = allow_select_all

    @property
    def choices(self):
        if isinstance(self.table_data, QuerySet):
            return self.table_data.values_list(self.value_field, self.value_name)

        # Default, we assume a list of dictionaries here with
        # 'value_field' and 'value_name' as keys
        return [(x[self.value_field], x[self.value_name]) for x in self.table_data]

    def get_select_all_checkbox_attrs(self, selected_values):
        """Attributes to add to the select all checkbox."""
        if not self.allow_select_all:
            return {}

        attrs = {}

        if selected_values:
            if len(selected_values) >= len(self.table_data):
                # All rows are selected, checkbox should display as checked
                attrs["checked"] = ""
        return attrs

    def get_accessible_label(self, record):
        """Return the accessible label to associate with the form checkbox.

        Defaults to `str(record)` for objects, or the value of a key self.value_name for dictionaries.

        This benefits users of assistive technology like screenreaders."""

        if isinstance(record, dict):
            obj_name = record.get(self.label_field)
        else:
            obj_name = getattr(record, self.label_field)

        return _("Select %(obj_name)s") % {"obj_name": obj_name}

    def get_value(self, record):
        """Value to use for the form checkbox."""

        if isinstance(record, dict):
            return record.get(self.value_field)

        return vars(record).get(self.value_field)

    def prepare_table_data(self, table_data):
        """Prepare table data with values necessary for the select checkbox."""

        for row in table_data:
            key = self.column_name
            value = self.get_value(row)

            if isinstance(row, dict):
                row[key] = value
            else:
                setattr(row, key, value)

        return table_data

    def _construct_sequence(self):
        table_kwargs = self.table_kwargs.copy()
        kwarg_sequence = table_kwargs.pop("sequence", ())
        meta_sequence = ()
        if hasattr(self.table_class, "Meta") and hasattr(
            self.table_class.Meta, "sequence"
        ):
            meta_sequence = getattr(self.table_class.Meta, "sequence")

        original_sequence = kwarg_sequence or meta_sequence

        # Reconstruct the sequence with the checkbox column at the start
        return (self.column_name, *original_sequence)

    def get_attrs(self, kwarg_attrs):
        """Get ``attrs`` keyword argument to pass to the table class."""
        meta_attrs = ()
        if hasattr(self.table_class, "Meta") and hasattr(
            self.table_class.Meta, "attrs"
        ):
            meta_attrs = getattr(self.table_class.Meta, "attrs")

        original_attrs = kwarg_attrs or meta_attrs
        attrs = {"data-tableselect": ""}
        attrs.update(original_attrs)

        return attrs

    def get_table(self, input_name, selected_values):
        table_kwargs = self.table_kwargs.copy()

        extra_columns = [
            (
                self.column_name,
                CheckBoxColumn(
                    verbose_name="",
                    input_name=input_name,
                    helper=self,
                    selected_values=selected_values,
                ),
            )
        ]
        extra_columns.extend(table_kwargs.pop("extra_columns", []))
        sequence = self._construct_sequence()
        attrs = self.get_attrs(table_kwargs.pop("attrs", {}))

        return self.table_class(
            # This table may never be ordered
            orderable=False,
            data=self.prepare_table_data(self.table_data),
            sequence=sequence,
            extra_columns=extra_columns,
            attrs=attrs,
            **table_kwargs,
        )

    def _get_media(self):
        return Media(js=[self.js_path])

    media = property(_get_media)
