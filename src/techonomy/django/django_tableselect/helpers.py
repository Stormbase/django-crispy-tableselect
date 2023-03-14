from django.utils.translation import gettext_lazy as _


class TableSelectHelper:
    """Helper that houses various features related to TableSelect."""

    value_field = "id"
    """Field of the record that holds the value to use in the form checkbox."""

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
