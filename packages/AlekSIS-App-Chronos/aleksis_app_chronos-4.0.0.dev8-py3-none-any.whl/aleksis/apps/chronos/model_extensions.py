from django.utils.translation import gettext_lazy as _

from aleksis.core.models import Group, Person

# Dynamically add extra permissions to Group and Person models in core
# Note: requires migrate afterwards
Group.add_permission(
    "view_group_timetable",
    _("Can view group timetable"),
)
Person.add_permission(
    "view_person_timetable",
    _("Can view person timetable"),
)
