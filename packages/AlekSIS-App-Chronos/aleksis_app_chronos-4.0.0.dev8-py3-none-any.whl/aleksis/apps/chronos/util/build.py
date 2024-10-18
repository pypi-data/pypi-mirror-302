from datetime import date, datetime, time

from aleksis.apps.chronos.models import LessonEvent, SupervisionEvent
from aleksis.core.models import Group, Person


def build_substitutions_list(wanted_day: date) -> tuple[list[dict], set[Person], set[Group]]:
    rows = []
    affected_teachers = set()
    affected_groups = set()

    lesson_events = LessonEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"amending": True},
        with_reference_object=True,
    )

    for lesson_event in lesson_events:
        affected_teachers.update(lesson_event["REFERENCE_OBJECT"].teachers.all())
        affected_teachers.update(lesson_event["REFERENCE_OBJECT"].amends.teachers.all())
        affected_groups.update(lesson_event["REFERENCE_OBJECT"].groups.all())
        affected_groups.update(lesson_event["REFERENCE_OBJECT"].amends.groups.all())

        row = {
            "type": "substitution",
            "sort_a": lesson_event["REFERENCE_OBJECT"].group_names,
            "sort_b": str(lesson_event["DTSTART"]),
            "el": lesson_event,
        }

        rows.append(row)

    supervision_events = SupervisionEvent.get_single_events(
        datetime.combine(wanted_day, time.min),
        datetime.combine(wanted_day, time.max),
        params={"amending": True},
        with_reference_object=True,
    )
    print(supervision_events)

    for supervision_event in supervision_events:
        affected_teachers.update(supervision_event["REFERENCE_OBJECT"].teachers.all())
        affected_teachers.update(supervision_event["REFERENCE_OBJECT"].amends.teachers.all())

        row = {
            "type": "supervision_substitution",
            "sort_a": "Z",
            "sort_b": str(supervision_event["DTSTART"]),
            "el": supervision_event,
        }

        rows.append(row)

    rows.sort(key=lambda row: row["sort_a"] + row["sort_b"])

    return rows, affected_teachers, affected_groups
