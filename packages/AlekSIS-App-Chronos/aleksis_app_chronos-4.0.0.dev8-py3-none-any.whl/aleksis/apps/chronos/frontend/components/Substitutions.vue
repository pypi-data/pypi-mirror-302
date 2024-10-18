<script setup>
import CRUDList from "aleksis.core/components/generic/CRUDList.vue";
import PrimaryActionButton from "aleksis.core/components/generic/buttons/PrimaryActionButton.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import GroupChip from "aleksis.core/components/group/GroupChip.vue";
import DateSelectFooter from "aleksis.core/components/generic/DateSelectFooter.vue";
</script>

<template>
  <c-r-u-d-list
    :gql-query="query"
    :gql-additional-query-args="{ date: date }"
    :get-gql-data="prepareList"
    :headers="headers"
    :disable-sort="true"
    :item-class="itemColor"
    :show-select="false"
    :enable-create="false"
    :enable-edit="false"
  >
    <template #title>
      <v-row class="d-flex align-center pt-2 pa-2">
        <v-card-title class="text-h4">
          {{ $d(new Date(date), "dateWithWeekday") }}
        </v-card-title>
        <v-spacer />
        <primary-action-button
          class="mr-4"
          i18n-key="chronos.substitutions.print"
          icon-text="$print"
          :to="{
            name: 'chronos.printSubstitutionsForDate',
            params: {
              date: date,
            },
          }"
        />
      </v-row>
      <v-card-text>
        <div v-if="affectedTeachers.length > 0">
          <strong>
            {{ $t("chronos.substitutions.affected_teachers") }}:
          </strong>
          <person-chip
            v-for="teacher in affectedTeachers"
            :key="teacher.id"
            class="ma-1"
            :person="teacher"
            :to="{
              name: 'chronos.timetableWithId',
              params: {
                type: 'person',
                id: teacher.id,
              },
            }"
          />
        </div>
        <div v-if="affectedGroups.length > 0">
          <strong> {{ $t("chronos.substitutions.affected_groups") }}: </strong>
          <!-- TODO: Link to group-timetable as well -->
          <!-- as soon as it becomes possible to resolve a -->
          <!-- group-timetable from the lesson-event group too. -->
          <group-chip
            v-for="group in affectedGroups"
            class="ma-1"
            :key="group.id"
            :group="group"
            format="short"
          />
        </div>
      </v-card-text>
    </template>
    <!-- TODO: Extract strike -> bold || normal pattern into own -->
    <!-- component and reuse? -->
    <template #groups="{ item: { oldGroups, newGroups } }">
      <span v-if="newGroups.length > 0">
        <span class="strike-through" v-for="g in oldGroups" :key="g.id">{{
          g.shortName
        }}</span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong v-for="g in newGroups" :key="g.id">{{ g.shortName }}</strong>
      </span>
      <span v-else v-for="g in oldGroups" :key="g.id">{{ g.shortName }}</span>
    </template>
    <template #time="{ item: { startSlot, endSlot, startTime, endTime } }">
      <span v-if="startSlot && endSlot && startSlot === endSlot">
        {{ startSlot }}.
      </span>
      <span v-else-if="startSlot && endSlot">
        {{ startSlot }}.–{{ endSlot }}.
      </span>
      <span v-else-if="startTime && endTime">
        {{ $d(new Date(startTime), "shortTime") }}
        –
        {{ $d(new Date(endTime), "shortTime") }}
      </span>
      <span v-else>{{ $t("chronos.substitutions.all_day") }}</span>
    </template>
    <template #teachers="{ item: { oldTeachers, newTeachers } }">
      <span v-if="newTeachers.length > 0">
        <span class="strike-through" v-for="t in oldTeachers" :key="t.id">
          {{ t.shortName || t.fullName }}
        </span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong v-for="t in newTeachers" :key="t.id">
          {{ t.shortName || t.fullName }}
        </strong>
      </span>
      <span v-else v-for="t in oldTeachers" :key="t.id">
        {{ t.shortName || t.fullName }}
      </span>
    </template>
    <template #subject="{ item: { oldSubject, newSubject } }">
      <span v-if="oldSubject === 'SUPERVISION'">
        {{ $t("chronos.substitutions.supervision") }}
      </span>
      <span v-else-if="newSubject">
        <span class="strike-through">{{ oldSubject }}</span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong>{{ newSubject }}</strong>
      </span>
      <span v-else>{{ oldSubject }}</span>
    </template>
    <template #rooms="{ item: { oldRooms, newRooms } }">
      <span v-if="newRooms.length > 0">
        <span class="strike-through" v-for="r in oldRooms" :key="r.id">{{
          r.shortName || r.name
        }}</span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong v-for="r in newRooms" :key="r.id">{{
          r.shortName || r.name
        }}</strong>
      </span>
      <span v-else v-for="r in oldRooms" :key="r.id">{{
        r.shortName || r.name
      }}</span>
    </template>
    <template #notes="{ item: { cancelled, notes } }">
      <v-chip v-if="cancelled" color="green" text-color="white">
        {{ $t("chronos.substitutions.cancelled") }}
      </v-chip>
      {{ notes }}
    </template>
    <template #no-data>
      {{ $t("chronos.substitutions.no_substitutions") }}
    </template>
    <template #footer>
      <!-- TODO: Skip over unneeded days; eg. weekends. -->
      <date-select-footer
        :value="date"
        @input="gotoDate"
        @prev="gotoDate(DateTime.fromISO(date).minus({ days: 1 }).toISODate())"
        @next="gotoDate(DateTime.fromISO(date).plus({ days: 1 }).toISODate())"
      />
    </template>
  </c-r-u-d-list>
</template>

<script>
import { substitutionsForDate } from "./substitutions.graphql";
import { DateTime } from "luxon";

export default {
  name: "Substitutions",
  props: {
    date: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      query: substitutionsForDate,
      affectedTeachers: [],
      affectedGroups: [],
      headers: [
        {
          text: this.$t("chronos.substitutions.groups"),
          value: "groups",
        },
        {
          text: this.$t("chronos.substitutions.time"),
          value: "time",
        },
        {
          text: this.$t("chronos.substitutions.teachers"),
          value: "teachers",
        },
        {
          text: this.$t("chronos.substitutions.subject"),
          value: "subject",
        },
        {
          text: this.$t("chronos.substitutions.rooms"),
          value: "rooms",
        },
        {
          text: this.$t("chronos.substitutions.notes"),
          value: "notes",
        },
      ],
    };
  },
  methods: {
    prepareList(data) {
      this.affectedTeachers = data.affectedTeachers;
      this.affectedGroups = data.affectedGroups;
      return data.substitutions;
    },
    itemColor(item) {
      return item.cancelled ? "green-text" : "";
    },
    gotoDate(date) {
      this.$router.push({
        name: "chronos.listSubstitutionsForDate",
        params: {
          date: date,
        },
      });
    },
  },
};
</script>

<style>
.green-text {
  color: green;
}
.strike-through {
  text-decoration: line-through;
}
</style>
