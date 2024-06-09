from django.core.exceptions import ImproperlyConfigured
from django.db import models
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
        label,
        value_field="id",
        *,
        table_kwargs={},
        allow_select_all=False,
    ):
        """
        Arguments:
        - column_name: str -- The name of the form field. The checkbox column is added to the table using this name.
        - table_class: Table -- Your table class, must inherit from ``django_tables2.Table``.
        - table_data: QuerySet|Iterable -- Data to use to populate the table. Can be a django QuerySet or an iterable of objects/dictionaries.
        - label: str | callable -- Field (or key in case of dict) to use from table data record to label the checkbox. If callable, it receives the object / dict and should return a string to label to checkbox with.
        - value_field: str -- Field (or key in case of dict) to use from table data record as checkbox value. Defaults to 'id'.

        Keyword arguments:
        - table_kwargs: dict -- Any extra keyword arguments to instantiate the table class with.
        - allow_select_all: bool -- Whether or not to show a 'select all' checkbox in the column header. Defaults to False.
        """
        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

        self.column_name = column_name
        self.table_class = table_class
        self.table_data = table_data
        self.label = label
        self.value_field = value_field
        self.table_kwargs = table_kwargs
        self.allow_select_all = allow_select_all

    @property
    def choices(self):
        if callable(self.label):
            return [(x[self.value_field], self.label(x)) for x in self.table_data]

        if isinstance(self.table_data, models.query.QuerySet) and isinstance(self.label, str):
            return self.table_data.values_list(self.value_field, self.label)

        return [(x[self.value_field], x[self.label]) for x in self.table_data]

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

        Uses the value specified by ``label`` as key for dictionaries or as attribute for objects.
        This benefits users of assistive technology like screenreaders."""

        if isinstance(record, dict):
            obj_name = record.get(self.label)
        else:
            obj_name = getattr(record, self.label)

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
        """Reconstructs the ``sequence`` argument for the table with the checkbox column in front."""
        table_kwargs = self.table_kwargs.copy()
        kwarg_sequence = table_kwargs.pop("sequence", ())
        meta_sequence = ()
        if hasattr(self.table_class, "Meta") and hasattr(self.table_class.Meta, "sequence"):
            meta_sequence = getattr(self.table_class.Meta, "sequence")

        original_sequence = kwarg_sequence or meta_sequence

        # Reconstruct the sequence with the checkbox column at the start
        return (self.column_name, *original_sequence)

    def get_attrs(self, kwarg_attrs):
        """Get ``attrs`` keyword argument to pass to the table class."""
        meta_attrs = ()
        if hasattr(self.table_class, "Meta") and hasattr(self.table_class.Meta, "attrs"):
            meta_attrs = getattr(self.table_class.Meta, "attrs")

        original_attrs = kwarg_attrs or meta_attrs
        attrs = {"data-tableselect": ""}
        attrs.update(original_attrs)

        return attrs

    def get_table(self, input_name, selected_values):
        """Return instance of the table class with checkbox column."""
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
            # This table may never be ordered.
            # We cannot guarantee ordering to work properly while still remembering what checkboxes are checked.
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
