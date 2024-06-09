from __future__ import annotations

from typing import TYPE_CHECKING

from django.template.loader import get_template
from django_tables2 import CheckBoxColumn as BaseCheckBoxColumn

if TYPE_CHECKING:
    from .helpers import TableSelectHelper

__all__ = [
    "CheckBoxColumn",
]


class CheckBoxColumn(BaseCheckBoxColumn):
    header_template = "django_crispy_tableselect/checkbox_column_header.html"

    def __init__(
        self,
        helper: TableSelectHelper,
        attrs={},
        input_name="",
        selected_values=[],
        **extra,
    ):
        self.helper = helper
        self.input_name = input_name
        self.selected_values = selected_values

        update_attrs = attrs.copy()

        td_input_attrs = attrs.get("td__input", {})
        th_input_attrs = attrs.get("th__input", {})
        update_attrs["td__input"] = {
            "name": input_name,
            "aria-label": lambda **kwargs: helper.get_accessible_label(kwargs.get("record")),
            **td_input_attrs,
        }
        update_attrs["th__input"] = {
            **self.helper.get_select_all_checkbox_attrs(selected_values),
            **th_input_attrs,
        }

        super().__init__(update_attrs, **extra)

    def is_checked(self, value, record):
        return str(value) in self.selected_values

    @property
    def header(self):
        default = {"type": "checkbox"}
        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = dict(default, **(specific or general or {}))

        template = get_template(self.header_template)
        return template.render({"attrs": attrs, "enable_select_all": self.helper.allow_select_all})
