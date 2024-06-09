class CrispyMediaMixin:
    """Mixin that gathers Media objects from Crispy layout objects and includes them in ``self.media``."""

    def _get_layout_nested_fields(self, layout):
        for field in layout.fields:
            yield field
            if hasattr(field, "fields"):
                yield from self._get_layout_nested_fields(field)

    @property
    def media(self):
        media = super().media
        if hasattr(self, "helper") and hasattr(self.helper, "layout"):
            for field in self._get_layout_nested_fields(self.helper.layout):
                if hasattr(field, "media"):
                    media += field.media
        return media
