from django.utils.translation import gettext_lazy as _
from .columns import CheckBoxColumn


class TableSelectHelper:
    """Helper that houses various features related to TableSelect."""

    value_field = "id"
    """Field of the record that holds the value to use in the form checkbox."""

    def __init__(self, column_name, table_class, table_data, table_kwargs):
        self.column_name = column_name
        self.table_class = table_class
        self.table_data = table_data
        self.table_kwargs = table_kwargs


    def get_accessible_label(self, record):
        """Return the accessible label to associate with the form checkbox.

        Defaults to `str(record)` for objects, or the value of a key `name` for dictionaries.

        This benefits users of assistive technology like screenreaders."""

        if isinstance(record, dict):
            obj_name = record.get("name")
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

        return self.table_class(
            # This table may never be ordered
            orderable=False,
            data=self.prepare_table_data(self.table_data),
            sequence=sequence,
            extra_columns=extra_columns,
            **table_kwargs,
        )
