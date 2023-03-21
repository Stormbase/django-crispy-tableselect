from django.utils.translation import gettext_lazy as _
from django_tables2 import CheckBoxColumn as BaseCheckBoxColumn

from .helpers import TableSelectHelper

__all__ = [
    "CheckBoxColumn",
]


class CheckBoxColumn(BaseCheckBoxColumn):
    def __init__(
        self,
        helper: TableSelectHelper,
        attrs={},
        input_name="",
        selected_values=[],
        **extra
    ):
        self.helper = helper
        self.selected_values = selected_values

        update_attrs = attrs.copy()

        td_input_attrs = attrs.get("td__input", {})
        update_attrs["td__input"] = {
            "name": input_name,
            "aria-label": lambda **kwargs: helper.get_accessible_label(
                kwargs.get("record")
            ),
            **td_input_attrs,
        }
        super().__init__(update_attrs, **extra)

    def is_checked(self, value, record):
        return str(value) in self.selected_values

    @property
    def header(self):
        # TODO: show bulk select checkbox
        return ""
