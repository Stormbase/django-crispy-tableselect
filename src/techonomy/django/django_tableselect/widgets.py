from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Widget
from django.utils.translation import gettext_lazy as _
from django_tables2 import Table

from .columns import CheckBoxColumn


class TableWidgetHelper:
    value_field = "pk"

    def get_accessible_label(self, record):
        return _("Select %(obj_name)s") % {"obj_name": str(record)}

    def get_value(self, record):
        return getattr(record, self.value_field)


class TableSelectMultipleWidget(Widget):
    template_name = "django_tableselect/table_select.html"

    def __init__(
        self,
        attrs={},
        data=(),
        choices=(),
        helper=TableWidgetHelper(),
        table_class=Table,
        table_kwargs={},
    ):
        self.table_class = table_class
        self.table_kwargs = table_kwargs
        self.data = list(data)
        self.choices = list(choices)
        self.helper = helper
        super().__init__(attrs)

        if not issubclass(table_class, Table):
            msg = f"{repr(table_class)} must be a subclass of {repr(Table)}"
            raise ImproperlyConfigured(msg)

    def options(self, name, value, attrs=None):
        options = []
        for index, record in enumerate(self.data):
            option_value = self.helper.get_value(record) or ""

            selected = False
            # Check if the option is present in the list of selected values
            if value and str(option_value) in value:
                selected = True
            options.append(
                self.create_option(name, option_value, selected, index, record, attrs)
            )

        return options

    def get_id_for_option(self, name, index="0"):
        return "id_{}_{}".format(name, index)

    def create_option(self, name, value, selected, index, record, attrs=None):
        option_attrs = self.build_attrs(self.attrs, attrs)
        id = self.get_id_for_option(name, index)

        return {
            "name": name,
            "id": id,
            "value": value,
            "selected": selected,
            "index": index,
            "attrs": option_attrs,
            "row_data": record,
        }

    def get_derived_table_class(self):
        class DerivedTable(self.table_class):
            class Meta(self.table_class.Meta):
                orderable = False

        return DerivedTable

    def get_table_instance(self, input_field_name, data):
        table_class = self.get_derived_table_class()

        extra_columns = [
            (
                input_field_name,
                CheckBoxColumn(
                    verbose_name="",
                    checked=lambda _, r: r.selected,
                    input_name=input_field_name,
                ),
            )
        ]
        extra_columns.extend(self.table_kwargs.pop("extra_columns", []))
        # Reconstruct the sequence with the checkbox in as the first item
        original_sequence = self.table_kwargs.pop("sequence", None) or getattr(
            table_class.Meta, "sequence", ()
        )
        sequence = (input_field_name, *original_sequence)

        return table_class(
            data=data,
            sequence=sequence,
            extra_columns=extra_columns,
            **self.table_kwargs,
        )

    def options_to_table_data(self, input_field_name, options):
        data = []
        for option in options:
            record = option["row_data"]
            setattr(record, input_field_name, option["value"])
            setattr(record, "selected", option["selected"])
            setattr(
                record, "_accessible_label", self.helper.get_accessible_label(record)
            )
            setattr(record, "_input_id", option["id"])
            data.append(record)
        return data

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)

        options = self.options(name, ctx["widget"]["value"], attrs)
        if options:
            options = list(options)
        else:
            options = []
        data = self.options_to_table_data(input_field_name=name, options=options)
        table = self.get_table_instance(input_field_name=name, data=data)
        ctx["table"] = table
        return ctx

    def value_from_datadict(self, data, files, name):
        getter = data.get
        try:
            getter = data.getlist
        except AttributeError:
            pass
        return getter(name)

    def format_value(self, value):
        """Return selected values as a list."""
        if value is None:
            return []
        if not isinstance(value, (tuple, list)):
            value = [value]
        return [str(v) if v is not None else "" for v in value]
