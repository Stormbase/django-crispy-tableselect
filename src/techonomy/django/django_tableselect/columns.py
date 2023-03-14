from django.utils.translation import gettext_lazy as _
from django_tables2 import CheckBoxColumn as BaseCheckBoxColumn

__all__ = [
    "CheckBoxColumn",
]


class CheckBoxColumn(BaseCheckBoxColumn):
    FALLBACK_ACCESSIBLE_LABEL = _("Select row")

    def aria_label(**kwargs):
        record = kwargs.get("record")
        return getattr(record, "_accessible_label", __class__.FALLBACK_ACCESSIBLE_LABEL)

    def input_id(**kwargs):
        record = kwargs.get("record")
        return getattr(record, "_input_id", None)

    def __init__(self, attrs={}, input_name="", checked=None, **extra):
        update_attrs = attrs.copy()

        td_input_attrs = attrs.get("td__input", {})
        update_attrs["td__input"] = {
            "name": input_name,
            "aria-label": __class__.aria_label,
            "id": __class__.input_id,
            **td_input_attrs,
        }
        super().__init__(update_attrs, checked, **extra)

    @property
    def header(self):
        # TODO: show bulk select checkbox
        return ""
