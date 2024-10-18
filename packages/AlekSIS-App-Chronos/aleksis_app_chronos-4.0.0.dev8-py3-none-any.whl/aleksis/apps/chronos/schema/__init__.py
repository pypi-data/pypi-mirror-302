import graphene
from graphene_django import DjangoObjectType

from aleksis.core.models import Group, Person, Room
from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
)
from aleksis.core.schema.group import GroupType
from aleksis.core.schema.person import PersonType
from aleksis.core.schema.room import RoomType

from ..models import LessonEvent
from ..util.build import build_substitutions_list
from ..util.chronos_helpers import get_groups, get_next_relevant_day, get_rooms, get_teachers


class TimetablePersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "short_name")
        skip_registry = True


class TimetableGroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("id", "name", "short_name")
        skip_registry = True


class TimetableRoomType(DjangoObjectType):
    class Meta:
        model = Room
        fields = ("id", "name", "short_name")
        skip_registry = True


class LessonEventType(DjangoObjectType):
    class Meta:
        model = LessonEvent
        fields = (
            "id",
            "title",
            "slot_number_start",
            "slot_number_end",
            "amends",
            "datetime_start",
            "datetime_end",
            "subject",
            "teachers",
            "groups",
            "rooms",
            "cancelled",
            "comment",
        )
        filter_fields = {
            "id": ["exact", "lte", "gte"],
        }

    amends = graphene.Field(lambda: LessonEventType, required=False)


class AmendLessonBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.edit_substitution_rule",)
        only_fields = (
            "amends",
            "datetime_start",
            "datetime_end",
            "subject",
            "teachers",
            "groups",
            "rooms",
            "cancelled",
            "comment",
        )

    @classmethod
    def before_save(cls, root, info, input, created_objects):  # noqa: A002
        super().before_save(root, info, input, created_objects)
        for obj in created_objects:
            obj.timezone = obj.amends.timezone
        return created_objects


class AmendLessonBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.edit_substitution_rule",)
        only_fields = ("id", "subject", "teachers", "groups", "rooms", "cancelled", "comment")

    @classmethod
    def before_save(cls, root, info, input, updated_objects):  # noqa: A002
        super().before_save(root, info, input, updated_objects)
        for obj in updated_objects:
            obj.timezone = obj.amends.timezone
        return updated_objects


class AmendLessonBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = LessonEvent
        permissions = ("chronos.delete_substitution_rule",)


class TimetableType(graphene.Enum):
    TEACHER = "teacher"
    GROUP = "group"
    ROOM = "room"


class TimetableObjectType(graphene.ObjectType):
    id = graphene.String()  # noqa
    obj_id = graphene.String()
    name = graphene.String()
    short_name = graphene.String()
    type = graphene.Field(TimetableType)  # noqa

    def resolve_obj_id(root, info, **kwargs):
        return root.id

    def resolve_id(root, info, **kwargs):
        return f"{root.type.value}-{root.id}"


class SubstitutionType(graphene.ObjectType):
    """This type contains the logic also contained in the pdf templates."""

    old_groups = graphene.List(GroupType)
    new_groups = graphene.List(GroupType)
    start_slot = graphene.Int()
    end_slot = graphene.Int()
    start_time = graphene.DateTime()
    end_time = graphene.DateTime()
    old_teachers = graphene.List(PersonType)
    new_teachers = graphene.List(PersonType)
    old_subject = graphene.String()
    new_subject = graphene.String()
    old_rooms = graphene.List(RoomType)
    new_rooms = graphene.List(RoomType)
    cancelled = graphene.Boolean()
    notes = graphene.String()

    # TODO: Extract old/new-pattern into own method and reuse?

    def resolve_old_groups(root, info):
        le = root["REFERENCE_OBJECT"]
        return le.amends.groups.all() or le.groups.all()

    def resolve_new_groups(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.groups.all() and le.amends.groups.all():
            return le.groups.all()
        else:
            return []

    def resolve_start_slot(root, info):
        return root["REFERENCE_OBJECT"].slot_number_start

    def resolve_end_slot(root, info):
        return root["REFERENCE_OBJECT"].slot_number_end

    def resolve_start_time(root, info):
        return root["DTSTART"].dt

    def resolve_end_time(root, info):
        return root["DTEND"].dt

    def resolve_old_teachers(root, info):
        le = root["REFERENCE_OBJECT"]
        return le.amends.teachers.all() or le.teachers.all()

    def resolve_new_teachers(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.teachers.all() and le.amends.teachers.all():
            return le.teachers.all()
        else:
            return []

    def resolve_old_subject(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.name == "supervision":
            return "SUPERVISION"
        elif not le.amends.subject and not le.subject:
            return le.amends.title
        else:
            subject = le.amends.subject or le.subject
            return subject.short_name or subject.name

    def resolve_new_subject(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.name == "supervision":
            return None
        elif not le.amends.subject and not le.subject:
            return le.title
        elif le.subject and le.amends.subject:
            return le.subject.short_name or le.subject.name
        else:
            return None

    def resolve_old_rooms(root, info):
        le = root["REFERENCE_OBJECT"]
        return le.amends.rooms.all() or le.rooms.all()

    def resolve_new_rooms(root, info):
        le = root["REFERENCE_OBJECT"]
        if le.rooms.all() and le.amends.rooms.all():
            return le.rooms.all()
        else:
            return []

    def resolve_cancelled(root, info):
        return root["REFERENCE_OBJECT"].cancelled

    def resolve_notes(root, info):
        return root["REFERENCE_OBJECT"].title or root["REFERENCE_OBJECT"].comment


class SubstitutionsForDateType(graphene.ObjectType):
    affected_teachers = graphene.List(PersonType)
    affected_groups = graphene.List(GroupType)
    substitutions = graphene.List(SubstitutionType)


class Query(graphene.ObjectType):
    timetable_teachers = graphene.List(TimetablePersonType)
    timetable_groups = graphene.List(TimetableGroupType)
    timetable_rooms = graphene.List(TimetableRoomType)
    available_timetables = graphene.List(TimetableObjectType)
    substitutions_for_date = graphene.Field(
        SubstitutionsForDateType,
        date=graphene.Date(),
    )

    def resolve_timetable_teachers(self, info, **kwargs):
        return get_teachers(info.context.user)

    def resolve_timetable_groups(self, info, **kwargs):
        return get_groups(info.context.user)

    def resolve_timetable_rooms(self, info, **kwargs):
        return get_rooms(info.context.user)

    def resolve_available_timetables(self, info, **kwargs):
        all_timetables = []
        for group in get_groups(info.context.user):
            all_timetables.append(
                TimetableObjectType(
                    id=group.id,
                    name=group.name,
                    short_name=group.short_name,
                    type=TimetableType.GROUP,
                )
            )

        for teacher in get_teachers(info.context.user):
            all_timetables.append(
                TimetableObjectType(
                    id=teacher.id,
                    name=teacher.full_name,
                    short_name=teacher.short_name,
                    type=TimetableType.TEACHER,
                )
            )

        for room in get_rooms(info.context.user):
            all_timetables.append(
                TimetableObjectType(
                    id=room.id, name=room.name, short_name=room.short_name, type=TimetableType.ROOM
                )
            )

        return all_timetables

    def resolve_substitutions_for_date(root, info, date):
        substitutions, affected_teachers, affected_groups = build_substitutions_list(
            get_next_relevant_day(date)
        )
        return SubstitutionsForDateType(
            affected_teachers=affected_teachers,
            affected_groups=affected_groups,
            substitutions=[sub["el"] for sub in substitutions],
        )


class Mutation(graphene.ObjectType):
    create_amend_lessons = AmendLessonBatchCreateMutation.Field()
    patch_amend_lessons = AmendLessonBatchPatchMutation.Field()
    delete_amend_lessons = AmendLessonBatchDeleteMutation.Field()
