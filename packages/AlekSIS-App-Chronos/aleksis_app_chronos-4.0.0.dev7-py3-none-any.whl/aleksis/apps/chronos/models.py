# flake8: noqa: DJ01
from __future__ import annotations

import itertools
from collections.abc import Iterable
from datetime import date
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.dispatch import receiver
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from reversion.models import Revision, Version

from aleksis.apps.chronos.managers import (
    LessonEventQuerySet,
    SupervisionEventQuerySet,
)
from aleksis.apps.chronos.util.change_tracker import _get_substitution_models, substitutions_changed
from aleksis.apps.cursus import models as cursus_models
from aleksis.apps.cursus.models import Course
from aleksis.apps.resint.models import LiveDocument
from aleksis.core.managers import (
    RecurrencePolymorphicManager,
)
from aleksis.core.mixins import (
    GlobalPermissionModel,
)
from aleksis.core.models import CalendarEvent, Group, Person, Room
from aleksis.core.util.core_helpers import get_site_preferences, has_person


class AutomaticPlan(LiveDocument):
    """Model for configuring automatically updated PDF substitution plans."""

    template = "chronos/substitutions_print.html"

    number_of_days = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Number of days shown in the plan"),
    )
    show_header_box = models.BooleanField(
        default=True,
        verbose_name=_("Show header box"),
        help_text=_("The header box shows affected teachers/groups."),
    )
    last_substitutions_revision = models.ForeignKey(
        to=Revision,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Revision which triggered the last update"),
        editable=False,
    )

    @property
    def current_start_day(self) -> date:
        """Get first day which should be shown in the PDF."""
        from aleksis.apps.chronos.util.chronos_helpers import get_next_relevant_day

        return get_next_relevant_day(timezone.now())

    @property
    def current_end_day(self) -> date:
        """Get last day which should be shown in the PDF."""
        from aleksis.apps.chronos.util.chronos_helpers import get_next_relevant_day

        day = self.current_start_day
        for _i in range(self.number_of_days - 1):
            day = get_next_relevant_day(day)
        return day

    def get_context_data(self) -> dict[str, Any]:
        """Get context data for generating the substitutions PDF."""
        from aleksis.apps.chronos.util.chronos_helpers import get_substitutions_context_data  # noqa

        context = get_substitutions_context_data(
            wanted_day=date.today(),
            number_of_days=self.number_of_days,
            show_header_box=self.show_header_box,
        )

        return context

    def check_update(self, revision: Revision):
        """Check if the PDF file has to be updated and do the update then."""
        if not self.last_substitutions_revision or (
            self.last_substitutions_revision != revision
            and revision.date_created > self.last_substitutions_revision.date_created
        ):
            content_types = ContentType.objects.get_for_models(*_get_substitution_models()).values()
            versions = Version.objects.filter(content_type__in=content_types)
            if self.last_substitutions_revision:
                versions = versions.filter(
                    revision__date_created__gt=self.last_substitutions_revision.date_created
                )
            update = False
            for version in versions:
                if not version.object:
                    # Object exists no longer, so we can skip this
                    continue

                # Check if the changed object is relevant for the time period of the PDF file
                if not version.object.amends:
                    return

                if version.object.datetime_start:
                    date_start = version.object.datetime_start.date()
                    date_end = version.object.datetime_end.date()
                else:
                    date_start = version.object.date_start
                    date_end = version.object.date_end

                if date_start <= self.current_end_day and date_end >= self.current_start_day:
                    update = True
                    break

            if update:
                self.update(triggered_manually=False)
                self.last_substitutions_revision = revision
                self.save()

    class Meta:
        verbose_name = _("Automatic plan")
        verbose_name_plural = _("Automatic plans")


@receiver(substitutions_changed)
def automatic_plan_signal_receiver(sender: Revision, versions: Iterable[Version], **kwargs):
    """Check all automatic plans for updates after substitutions changed."""
    for automatic_plan in AutomaticPlan.objects.all():
        automatic_plan.check_update(sender)


class ChronosGlobalPermissions(GlobalPermissionModel):
    class Meta:
        managed = False
        permissions = (
            ("view_all_room_timetables", _("Can view all room timetables")),
            ("view_all_group_timetables", _("Can view all group timetables")),
            ("view_all_person_timetables", _("Can view all person timetables")),
            ("view_timetable_overview", _("Can view timetable overview")),
            ("view_substitutions", _("Can view substitutions table")),
        )


class LessonEvent(CalendarEvent):
    """Calendar feed for lessons."""

    name = "lesson"
    verbose_name = _("Lessons")

    objects = RecurrencePolymorphicManager.from_queryset(LessonEventQuerySet)()

    title = models.CharField(verbose_name=_("Name"), max_length=255, blank=True)

    slot_number_start = models.PositiveSmallIntegerField(
        verbose_name=_("Start slot number"), blank=True, null=True
    )
    slot_number_end = models.PositiveSmallIntegerField(
        verbose_name=_("End slot number"), blank=True, null=True
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course"), null=True, blank=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name="lesson_events",
        verbose_name=_("Groups"),
        blank=True,
    )

    rooms = models.ManyToManyField(
        Room,
        verbose_name=_("Rooms"),
        related_name="lesson_events",
        blank=True,
    )
    teachers = models.ManyToManyField(
        Person,
        verbose_name=_("Teachers"),
        related_name="lesson_events_as_teacher",
        blank=True,
    )
    subject = models.ForeignKey(
        cursus_models.Subject,
        on_delete=models.CASCADE,
        verbose_name=_("Subject"),
        related_name="lesson_events",
        blank=True,
        null=True,
    )

    cancelled = models.BooleanField(
        default=False,
        verbose_name=_("Cancelled"),
    )

    comment = models.TextField(
        verbose_name=_("Comment"),
        blank=True,
    )

    @property
    def actual_groups(self: LessonEvent) -> QuerySet[Group]:
        """Get list of the groups of this lesson event."""
        return self.amends.groups.all() if self.amends else self.groups.all()

    @property
    def all_members(self: LessonEvent) -> list[Person]:
        """Get list of all group members for this lesson event."""
        return list(itertools.chain(*[list(g.members.all()) for g in self.actual_groups]))

    @property
    def all_teachers(self: LessonEvent) -> list[Person]:
        """Get list of all teachers for this lesson event."""
        all_teachers = list(self.teachers.all())
        if self.amends:
            all_teachers += list(self.amends.teachers.all())
        return all_teachers

    @property
    def group_names(self: LessonEvent) -> str:
        """Get comma-separated string with all group names."""
        return ", ".join([g.name for g in self.actual_groups])

    @property
    def teacher_names(self: LessonEvent) -> str:
        """Get comma-separated string with all teacher names."""
        return ", ".join([t.full_name for t in self.teachers.all()])

    @property
    def room_names(self: LessonEvent) -> str:
        """Get comma-separated string with all room names."""
        return ", ".join([r.name for r in self.rooms.all()])

    @property
    def room_names_with_amends(self: LessonEvent) -> str:
        """Get comma-separated string with all room names (including amends)."""
        my_room_names = self.room_names
        amended_room_names = self.amends.room_names if self.amends else ""

        if my_room_names and amended_room_names:
            return _("{} (instead of {})").format(my_room_names, amended_room_names)
        elif not my_room_names and amended_room_names:
            return amended_room_names
        return my_room_names

    @property
    def teacher_names_with_amends(self: LessonEvent) -> str:
        """Get comma-separated string with all teacher names (including amends)."""
        my_teacher_names = self.teacher_names
        amended_teacher_names = self.amends.teacher_names if self.amends else ""

        if my_teacher_names and amended_teacher_names:
            return _("{} (instead of {})").format(my_teacher_names, amended_teacher_names)
        elif not my_teacher_names and amended_teacher_names:
            return amended_teacher_names
        return my_teacher_names

    @property
    def subject_name_with_amends(self: LessonEvent) -> str:
        """Get formatted subject name (including amends)."""
        my_subject = self.subject.name if self.subject else ""
        amended_subject = self.amends.subject.name if self.amends and self.amends.subject else ""

        if my_subject and amended_subject:
            return _("{} (instead of {})").format(my_subject, amended_subject)
        elif not my_subject and amended_subject:
            return amended_subject
        elif my_subject:
            return my_subject
        return _("Lesson")

    @classmethod
    def value_title(cls, reference_object: LessonEvent, request: HttpRequest | None = None) -> str:
        """Get the title of the lesson event."""
        if reference_object.title:
            return reference_object.title
        elif reference_object.subject or (
            reference_object.amends and reference_object.amends.subject
        ):
            title = reference_object.subject_name_with_amends
            if request and request.user.person in reference_object.teachers.all():
                title += " · " + reference_object.group_names
            elif request:
                title += " · " + reference_object.teacher_names_with_amends
            else:
                title += (
                    f" · {reference_object.group_names} · "
                    + f"{reference_object.teacher_names_with_amends}"
                )
            if reference_object.rooms.all().exists():
                title += " · " + reference_object.room_names_with_amends
            return title

        return _("Lesson")

    @classmethod
    def value_description(
        cls, reference_object: LessonEvent, request: HttpRequest | None = None
    ) -> str:
        """Get the description of the lesson event."""
        return render_to_string("chronos/lesson_event_description.txt", {"event": reference_object})

    @classmethod
    def get_color(cls, request: HttpRequest | None = None) -> str:
        return get_site_preferences()["chronos__lesson_color"]

    @classmethod
    def value_color(cls, reference_object: LessonEvent, request: HttpRequest | None = None) -> str:
        """Get the color of the lesson event."""
        if reference_object.cancelled:
            return "#eeeeee"
        if reference_object.subject:
            return reference_object.subject.colour_bg
        if reference_object.amends and reference_object.amends.subject:
            return reference_object.amends.subject.colour_bg
        return super().value_color(reference_object, request)

    @classmethod
    def value_attendee(
        cls, reference_object: LessonEvent, request: HttpRequest | None = None
    ) -> str:
        """Get the attendees of the lesson event."""
        # Only teachers due to privacy concerns
        attendees = [t.get_vcal_address(role="CHAIR") for t in reference_object.teachers.all()]
        return [a for a in attendees if a]

    @classmethod
    def value_location(
        cls, reference_object: LessonEvent, request: HttpRequest | None = None
    ) -> str:
        """Get the location of the lesson event."""
        return reference_object.room_names_with_amends

    @classmethod
    def value_status(cls, reference_object: LessonEvent, request: HttpRequest | None = None) -> str:
        """Get the status of the lesson event."""
        if reference_object.cancelled:
            return "CANCELLED"
        return "CONFIRMED"

    @classmethod
    def value_meta(cls, reference_object: LessonEvent, request: HttpRequest | None = None) -> str:
        """Get the meta of the lesson event.

        These information will be primarly used in our own calendar frontend.
        """

        return {
            "id": reference_object.id,
            "amended": bool(reference_object.amends),
            "amends": cls.value_meta(reference_object.amends, request)
            if reference_object.amends
            else None,
            "title": reference_object.title,
            "slot_number_start": reference_object.slot_number_start,
            "slot_number_end": reference_object.slot_number_end,
            "teachers": [
                {
                    "id": t.pk,
                    "first_name": t.first_name,
                    "last_name": t.last_name,
                    "full_name": t.full_name,
                    "short_name": t.short_name,
                }
                for t in reference_object.teachers.all()
            ],
            "is_teacher": request.user.person in reference_object.all_teachers if request else None,
            "groups": [
                {"id": g.pk, "name": g.name, "short_name": g.short_name}
                for g in reference_object.actual_groups
            ],
            "is_member": request.user.person in reference_object.all_members if request else None,
            "rooms": [
                {"id": r.pk, "name": r.name, "short_name": r.short_name}
                for r in reference_object.rooms.all()
            ],
            "subject": {
                "id": reference_object.subject.pk,
                "name": reference_object.subject.name,
                "short_name": reference_object.subject.short_name,
                "colour_fg": reference_object.subject.colour_fg,
                "colour_bg": reference_object.subject.colour_bg,
            }
            if reference_object.subject
            else None,
            "comment": reference_object.comment,
            "cancelled": reference_object.cancelled,
        }

    @classmethod
    def get_objects(
        cls,
        request: HttpRequest | None = None,
        params: dict[str, any] | None = None,
        no_effect: bool = False,
        **kwargs,
    ) -> Iterable:
        """Return all objects that should be included in the calendar."""
        if no_effect:
            return super().get_objects(request, params, **kwargs)
        objs = (
            super()
            .get_objects(request, params, **kwargs)
            .not_instance_of(SupervisionEvent)
            .select_related("subject", "course")
            .prefetch_related("groups", "teachers", "rooms", "groups__members")
        )

        if request and not has_person(request.user):
            raise PermissionDenied()

        if params:
            obj_id = int(params.get("id", 0))
            type_ = params.get("type", None)
            not_amended = params.get("not_amended", False)
            not_amending = params.get("not_amending", False)
            amending = params.get("amending", False)
            own = params.get("own", False)

            if not_amended:
                objs = objs.not_amended()

            if not_amending:
                objs = objs.not_amending()

            if amending:
                objs = objs.amending()

            if request and "own" in params:
                if own:
                    objs = objs.for_person(request.user.person)
                else:
                    objs = objs.related_to_person(request.user.person)

            if type_ and obj_id:
                if type_ == "TEACHER":
                    return objs.for_teacher(obj_id)
                elif type_ == "PARTICIPANT":
                    return objs.for_participant(obj_id)
                elif type_ == "GROUP":
                    return objs.for_group(obj_id)
                elif type_ == "ROOM":
                    return objs.for_room(obj_id)
                elif type_ == "COURSE":
                    return objs.for_course(obj_id)

            if "own" in params:
                return objs
        if request:
            return objs.for_person(request.user.person)
        return objs

    class Meta:
        verbose_name = _("Lesson Event")
        verbose_name_plural = _("Lesson Events")


class SupervisionEvent(LessonEvent):
    """Calendar feed for supervisions."""

    name = "supervision"
    verbose_name = _("Supervisions")

    objects = RecurrencePolymorphicManager.from_queryset(SupervisionEventQuerySet)()

    @classmethod
    def value_title(cls, reference_object: LessonEvent, request: HttpRequest | None = None) -> str:
        """Get the title of the event."""

        return _("Supervision: {}").format(reference_object.room_names)

    @classmethod
    def value_description(
        cls, reference_object: LessonEvent, request: HttpRequest | None = None
    ) -> str:
        return render_to_string(
            "chronos/supervision_event_description.txt", {"event": reference_object}
        )

    @classmethod
    def get_color(cls, request: HttpRequest | None = None) -> str:
        return get_site_preferences()["chronos__supervision_color"]

    @classmethod
    def get_objects(
        cls, request: HttpRequest | None = None, params: dict[str, any] | None = None, **kwargs
    ) -> Iterable:
        """Return all objects that should be included in the calendar."""
        objs = super().get_objects(request, params, no_effect=True, **kwargs)
        if params:
            obj_id = int(params.get("id", 0))
            type_ = params.get("type", None)
            not_amended = params.get("not_amended", False)
            not_amending = params.get("not_amending", False)
            amending = params.get("amending", False)

            if not_amended:
                objs = objs.not_amended()

            if not_amending:
                objs = objs.not_amending()

            if amending:
                objs = objs.amending()

            if type_ and obj_id:
                if type_ == "TEACHER":
                    return objs.for_teacher(obj_id)
                elif type_ == "GROUP":
                    return objs.for_group(obj_id)
                elif type_ == "ROOM":
                    return objs.for_room(obj_id)
        if request:
            return objs.for_person(request.user.person)
        return objs
