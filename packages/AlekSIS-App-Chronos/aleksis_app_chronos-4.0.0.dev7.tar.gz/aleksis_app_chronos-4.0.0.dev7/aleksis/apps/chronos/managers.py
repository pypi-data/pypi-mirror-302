from enum import Enum
from typing import Optional, Union

from django.db.models import Q

from aleksis.apps.cursus.models import Course
from aleksis.core.managers import (
    RecurrencePolymorphicQuerySet,
)
from aleksis.core.models import Group, Person, Room


class TimetableType(Enum):
    """Enum for different types of timetables."""

    GROUP = "group"
    TEACHER = "teacher"
    ROOM = "room"

    @classmethod
    def from_string(cls, s: Optional[str]):
        return cls.__members__.get(s.upper())


class LessonEventQuerySet(RecurrencePolymorphicQuerySet):
    """Queryset with special query methods for lesson events."""

    def for_teacher(self, teacher: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person as teacher (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(teachers=teacher))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(teachers=teacher) | Q(pk__in=amended)).distinct()

    def for_participant(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events the person participates in (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & Q(groups__members=person)).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(groups__members=person) | Q(pk__in=amended)).distinct()

    def for_group(self, group: Union[int, Group]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain group (including amends/as parent group)."""
        amended = self.filter(
            Q(amended_by__isnull=False) & (Q(groups=group) | Q(groups__parent_groups=group))
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(groups=group) | Q(groups__parent_groups=group) | Q(pk__in=amended)
        ).distinct()

    def for_room(self, room: Union[int, Room]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain room (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(rooms=room))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(rooms=room) | Q(pk__in=amended)).distinct()

    def for_course(self, course: Union[int, Course]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain course (including amends)."""
        amended = self.filter(Q(amended_by__isnull=False) & (Q(course=course))).values_list(
            "amended_by__pk", flat=True
        )
        return self.filter(Q(course=course) | Q(pk__in=amended)).distinct()

    def for_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events for a certain person (as teacher/participant, including amends)."""
        amended = self.filter(
            Q(amended_by__isnull=False) & (Q(teachers=person) | Q(groups__members=person))
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(teachers=person) | Q(groups__members=person) | Q(pk__in=amended)
        ).distinct()

    def related_to_person(self, person: Union[int, Person]) -> "LessonEventQuerySet":
        """Get all lesson events a certain person is allowed to see.

        This includes all lesson events the person is assigned to as
        teacher/participant/group owner/parent group owner,
        including those amended.
        """
        amended = self.filter(
            Q(amended_by__isnull=False)
            & (
                Q(teachers=person)
                | Q(groups__members=person)
                | Q(groups__owners=person)
                | Q(groups__parent_groups__owners=person)
            )
        ).values_list("amended_by__pk", flat=True)
        return self.filter(
            Q(teachers=person)
            | Q(groups__members=person)
            | Q(groups__owners=person)
            | Q(groups__parent_groups__owners=person)
            | Q(pk__in=amended)
        ).distinct()

    def not_amended(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amended."""
        return self.filter(amended_by__isnull=True)

    def not_amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are not amending other events."""
        return self.filter(amends__isnull=True)

    def amending(self) -> "LessonEventQuerySet":
        """Get all lesson events that are amending other events."""
        return self.filter(amends__isnull=False)


class SupervisionEventQuerySet(LessonEventQuerySet):
    pass
