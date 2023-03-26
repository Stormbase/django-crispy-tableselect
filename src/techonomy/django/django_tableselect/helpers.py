from django.core.exceptions import ImproperlyConfigured
from django.db.models.query import QuerySet
from django.forms.widgets import Media
from django.utils.translation import gettext_lazy as _
from django_tables2 import Table

from .columns import CheckBoxColumn


class TableSelectHelper:
    """Helper that houses various features related to TableSelect."""

    # Field of the record that holds the value to use in the form checkbox.
    value_field = "id"

    # Field of the record that holds the name to use in the form checkbox.
    value_name = "name"

    # Path to javascript static file
    js_path = "django_tableselect/tableselect.js"

    def __init__(
        self,
        column_name,
        table_class,
        table_data,
        table_kwargs={},
        *,
        allow_bulk_select=True,
    ):
        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

        self.column_name = column_name
        self.table_class = table_class
        self.table_data = table_data
        self.table_kwargs = table_kwargs
        self.allow_bulk_select = allow_bulk_select

    @property
    def choices(self):
        if isinstance(self.table_data, QuerySet):
            return self.table_data.values_list(self.value_field, self.value_name)

        # Default, we assume a list of dictionaries here with
        # 'value_field' and 'value_name' as keys
        return [(x[self.value_field], x[self.value_name]) for x in self.table_data]

    def get_bulk_select_attrs(self, selected_values):
        """Attributes to add to the bulk select checkbox."""

        if not self.allow_bulk_select:
            return {}

        attrs = {
            # Data attribute for javascript to find this element
            "data-bulk-select": "",
        }

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
            obj_name = record.get(self.value_name)
        else:
            obj_name = str(record)

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

        attrs = table_kwargs.pop("attrs", {})

        # Selector for js initializer
        attrs["data-tableselect"] = ""

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
        media = Media()
        if self.allow_bulk_select:
            media = Media(js=[self.js_path])
        return media

    media = property(_get_media)
