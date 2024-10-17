from rules import add_perm

from aleksis.core.util.predicates import (
    has_global_perm,
    has_object_perm,
    has_person,
)

from .util.predicates import has_any_timetable_object, has_timetable_perm

# View timetable overview
view_timetable_overview_predicate = has_person & (
    has_any_timetable_object | has_global_perm("chronos.view_timetable_overview")
)
add_perm("chronos.view_timetable_overview_rule", view_timetable_overview_predicate)

# View timetable
view_timetable_predicate = has_person & has_timetable_perm
add_perm("chronos.view_timetable_rule", view_timetable_predicate)


# Edit substition
edit_substitution_predicate = has_person & (
    has_global_perm("chronos.change_lessonevent") | has_object_perm("chronos.change_lessonevent")
)
add_perm("chronos.edit_substitution_rule", edit_substitution_predicate)

# Delete substitution
delete_substitution_predicate = has_person & (
    has_global_perm("chronos.delete_lessonevent") | has_object_perm("chronos.delete_lessonevent")
)
add_perm("chronos.delete_substitution_rule", delete_substitution_predicate)

# View substitutions
view_substitutions_predicate = has_person & (has_global_perm("chronos.view_substitutions"))
add_perm("chronos.view_substitutions_rule", view_substitutions_predicate)

# View parent menu entry
view_menu_predicate = has_person & (view_timetable_overview_predicate)
add_perm("chronos.view_menu_rule", view_menu_predicate)
