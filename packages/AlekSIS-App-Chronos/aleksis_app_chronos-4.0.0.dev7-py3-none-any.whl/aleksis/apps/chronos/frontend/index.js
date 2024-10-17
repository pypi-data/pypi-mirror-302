import { hasPersonValidator } from "aleksis.core/routeValidators";
import Timetable from "./components/Timetable.vue";

export default {
  meta: {
    inMenu: true,
    titleKey: "chronos.menu_title",
    icon: "mdi-school-outline",
    iconActive: "mdi-school",
    permission: "chronos.view_menu_rule",
  },
  children: [
    {
      path: "timetable/",
      component: Timetable,
      name: "chronos.timetable",
      meta: {
        inMenu: true,
        titleKey: "chronos.timetable.menu_title",
        toolbarTitle: "chronos.timetable.menu_title",
        icon: "mdi-grid",
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
    },
    {
      path: "timetable/:type/:id/",
      component: Timetable,
      name: "chronos.timetableWithId",
      meta: {
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
      children: [
        {
          path: ":view(month|week|day)/:year(\\d\\d\\d\\d)/:month(\\d\\d)/:day(\\d\\d)/",
          component: Timetable,
          name: "chronos.timetableWithIdAndParams",
          meta: {
            permission: "chronos.view_timetable_overview_rule",
            fullWidth: true,
          },
        },
      ],
    },
    {
      path: "substitutions/print/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "chronos.substitutions",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "substitutions/print/:date/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "chronos.substitutionsByDate",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
  ],
};
