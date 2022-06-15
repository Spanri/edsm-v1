import Vue from "vue";
import Vuex from "vuex";
import Addit from "./addit";
import Auth from "./auth";
import Doc from "./doc";
import User from "./user";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: { Addit, Auth, Doc, User },
});
