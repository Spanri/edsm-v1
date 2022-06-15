import Vue from "vue";
import Router from "vue-router";
import store from "@/store";

Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/auth");
};

const ifAdmin = (to, from, next) => {
  if (store.getters.getProfile.is_staff) {
    next();
    return;
  }
  next("/");
};

const router = new Router({
  mode: "history",
  base: "/app",
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("@/views/Home"),
      children: [
        {
          path: "",
          redirect: "/documents/all",
        },
        {
          path: "documents/:id",
          name: "Grid",
          component: () => import("@/views/addit/Grid"),
          meta: { title: "Главная, СЭД МТУСИ" },
          props: {
            columns: [
              { key: "reg", title: "№" },
              { key: "title", title: "НАЗВАНИЕ" },
              { key: "full_name", title: "ВЛАДЕЛЕЦ" },
              { key: "date_doc", title: "ДАТА ДОБАВЛЕНИЯ" },
            ],
          },
        },
      ],
      beforeEnter: ifAuthenticated,
    },
    {
      path: "/auth",
      name: "Auth",
      component: () => import("@/views/Auth"),
      meta: { title: "Вход, СЭД МТУСИ" },
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: "/help",
      name: "Help",
      component: () => import("@/views/Help"),
      meta: { title: "Помощь, СЭД МТУСИ" },
    },
    {
      path: "/add-doc",
      name: "AddDoc",
      component: () => import("@/views/docs/AddDoc"),
      meta: { title: "Добавить документ, СЭД МТУСИ" },
      beforeEnter: ifAuthenticated,
    },
    {
      path: "/document/:id",
      name: "Document",
      component: () => import("@/views/docs/Document"),
      meta: { title: "Документ, СЭД МТУСИ" },
      props: true,
      beforeEnter: ifAuthenticated,
    },
    {
      path: "/document/:id/edit",
      name: "EditDocument",
      component: () => import("@/views/docs/EditDocument"),
      meta: { title: "Редактировать документ, СЭД МТУСИ" },
      props: true,
      beforeEnter: ifAuthenticated,
    },
    {
      path: "/profile",
      component: () => import("@/views/profile/Profile"),
      children: [
        {
          path: "",
          redirect: "/profile/notif",
        },
        {
          path: "notif",
          name: "Notif",
          component: () => import("@/views/addit/Grid"),
          meta: { title: "Уведомления, СЭД МТУСИ" },
          props: {
            id: "notif",
            columns: [
              { key: "initiator", title: "ИНИЦИАТОР" },
              { key: "title", title: "ДОКУМЕНТ" },
              { key: "message", title: "СООБЩЕНИЕ" },
              { key: "date_notif", title: "ДАТА" },
              { key: "file_cabinet", title: "КАРТОТЕКА" },
            ],
          },
        },
        {
          path: "edit",
          name: "EditProfile",
          component: () => import("@/views/profile/EditProfile"),
          meta: { title: "Редактировать профиль, СЭД МТУСИ" },
        },
        {
          path: "admin",
          name: "Admin",
          component: () => import("@/views/profile/Adm"),
          meta: { title: "Администрирование профилей, СЭД МТУСИ" },
          beforeEnter: ifAdmin,
        },
      ],
      beforeEnter: ifAuthenticated,
    },
    {
      path: "/404",
      component: () => import("@/views/NotFound"),
      meta: { title: "Страница не найдена, СЭД МТУСИ" },
    },
    {
      path: "*",
      redirect: "/404",
    },
  ],
});

/**
 * При переходе на новую страницу меняем заголовок во вкладке
 */
router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;
