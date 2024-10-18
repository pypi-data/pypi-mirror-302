from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING, Optional

from django.db.models import Count, Q

from guardian.core import ObjectPermissionChecker

from aleksis.core.models import Announcement, Group, Person, Room
from aleksis.core.util.core_helpers import get_site_preferences
from aleksis.core.util.predicates import check_global_permission

from .build import build_substitutions_list

if TYPE_CHECKING:
    from django.contrib.auth import get_user_model

    User = get_user_model()  # noqa


def get_teachers(user: "User"):
    """Get the teachers whose timetables are allowed to be seen by current user."""
    checker = ObjectPermissionChecker(user)

    teachers = (
        Person.objects.annotate(lessons_count=Count("lesson_events_as_teacher"))
        .filter(lessons_count__gt=0)
        .order_by("short_name", "last_name")
    )

    if not check_global_permission(user, "chronos.view_all_person_timetables"):
        checker.prefetch_perms(teachers)

        wanted_teachers = set()

        for teacher in teachers:
            if checker.has_perm("core.view_person_timetable", teacher):
                wanted_teachers.add(teacher.pk)

        teachers = teachers.filter(Q(pk=user.person.pk) | Q(pk__in=wanted_teachers))

    teachers = teachers.distinct()

    return teachers


def get_groups(user: "User"):
    """Get the groups whose timetables are allowed to be seen by current user."""
    checker = ObjectPermissionChecker(user)

    groups = (
        Group.objects.for_current_school_term_or_all()
        .annotate(
            lessons_count=Count("lesson_events"),
            child_lessons_count=Count("child_groups__lesson_events"),
        )
        .filter(Q(lessons_count__gt=0) | Q(child_lessons_count__gt=0))
    )

    group_types = get_site_preferences()["chronos__group_types_timetables"]

    if group_types:
        groups = groups.filter(group_type__in=group_types)

    groups = groups.order_by("short_name", "name")

    if not check_global_permission(user, "chronos.view_all_group_timetables"):
        checker.prefetch_perms(groups)

        wanted_classes = set()

        for _class in groups:
            if checker.has_perm("core.view_group_timetable", _class):
                wanted_classes.add(_class.pk)

        groups = groups.filter(
            Q(pk__in=wanted_classes) | Q(members=user.person) | Q(owners=user.person)
        )
        if user.person.primary_group:
            groups = groups.filter(Q(pk=user.person.primary_group.pk))

    groups = groups.distinct()

    return groups


def get_rooms(user: "User"):
    """Get the rooms whose timetables are allowed to be seen by current user."""
    checker = ObjectPermissionChecker(user)

    rooms = (
        Room.objects.annotate(lessons_count=Count("lesson_events"))
        .filter(lessons_count__gt=0)
        .order_by("short_name", "name")
    )

    if not check_global_permission(user, "chronos.view_all_room_timetables"):
        checker.prefetch_perms(rooms)

        wanted_rooms = set()

        for room in rooms:
            if checker.has_perm("core.view_room_timetable", room):
                wanted_rooms.add(room.pk)

        rooms = rooms.filter(Q(pk__in=wanted_rooms))

    rooms = rooms.distinct()

    return rooms


def get_substitutions_context_data(
    wanted_day: date,
    number_of_days: Optional[int] = None,
    show_header_box: Optional[bool] = None,
):
    """Get context data for the substitutions table."""
    context = {}

    day_number = (
        number_of_days or get_site_preferences()["chronos__substitutions_print_number_of_days"]
    )
    show_header_box = (
        show_header_box
        if show_header_box is not None
        else get_site_preferences()["chronos__substitutions_show_header_box"]
    )
    day_contexts = {}

    day = get_next_relevant_day(wanted_day)
    for _i in range(day_number):
        day_contexts[day] = {"day": day}

        subs, affected_teachers, affected_groups = build_substitutions_list(day)
        day_contexts[day]["substitutions"] = subs

        day_contexts[day]["announcements"] = Announcement.objects.on_date(day)

        if show_header_box:
            day_contexts[day]["affected_teachers"] = sorted(
                affected_teachers, key=lambda t: t.short_name or t.full_name
            )
            day_contexts[day]["affected_groups"] = affected_groups

        day = get_next_relevant_day(day + timedelta(days=1))

    context["days"] = day_contexts

    return context


def get_next_relevant_day(current: datetime | date) -> date:
    """Get next relevant day for substitution plans."""
    relevant_days = get_site_preferences()["chronos__substitutions_relevant_days"]
    change_time = get_site_preferences()["chronos__substitutions_day_change_time"]

    if isinstance(current, datetime):
        current_day = current.date()
        if current.time() > change_time:
            current_day += timedelta(days=1)
    else:
        current_day = current

    while str(current_day.weekday()) not in relevant_days:
        current_day += timedelta(days=1)

    return current_day
