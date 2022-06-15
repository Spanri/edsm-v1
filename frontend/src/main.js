import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

/**
 * Для валидации форм
 */
import VeeValidate from "vee-validate";
Vue.use(VeeValidate);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
