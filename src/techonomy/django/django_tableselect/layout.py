from crispy_forms import layout
from crispy_forms.utils import TEMPLATE_PACK
from django.template.loader import render_to_string


class TableSelect(layout.TemplateNameMixin):
    template = "django_tableselect/table_select.html"

    def __init__(
        self,
        name,
        helper,
        **kwargs,
    ):
        self.name = name
        self.helper = helper

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        bound_field = form[self.name]

        selected_values = bound_field.value()

        html_name = bound_field.html_name
        context.update(
            {
                "table": self.helper.get_table(
                    input_name=html_name, selected_values=selected_values
                )
            }
        )
        return render_to_string(template, context.flatten())
