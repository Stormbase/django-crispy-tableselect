from crispy_forms import layout
from crispy_forms.utils import TEMPLATE_PACK
from django.template.loader import render_to_string


class TableSelect(layout.TemplateNameMixin):
    template = "django_crispy_tableselect/table_select.html"

    def __init__(
        self,
        name,
        helper,
        **kwargs,
    ):
        self.name = name
        self.helper = helper

    @property
    def media(self):
        # Make the helper media easily available to the form
        return self.helper.media

    def format_value(self, value):
        """Return selected values as a list."""
        if value is None:
            return []
        if not isinstance(value, (tuple, list)):
            value = [value]
        return [str(v) if v is not None else "" for v in value]

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        bound_field = form[self.name]

        selected_values = self.format_value(bound_field.value())

        html_name = bound_field.html_name
        context.update({"table": self.helper.get_table(input_name=html_name, selected_values=selected_values)})
        return render_to_string(template, context.flatten())
