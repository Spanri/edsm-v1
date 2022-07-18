import {
  AUTH_REQUEST,
  AUTH_TOKEN,
  AUTH_AUTH,
  USER_REQUEST,
  AUTH_LOGOUT,
  AUTH_SIGNUP,
  DOCS_FILE_CABINET,
  DOCS_SUCCESS,
  DOCS_REQUEST,
  path,
} from "./mutation-types";
import httpClient from "./_httpClient";

export default {
  state: {
    token: localStorage.getItem("user-token") || "",
    auth: "",
  },

  getters: {
    token: (state) => state.token,
    auth: (state) => state.auth,
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    [AUTH_SIGNUP]: async ({ commit, dispatch, rootState }, data) => {
      try {
        const resp = await httpClient.post("api/users/send_invite/", data);

        return resp.data.password;
      } catch (err) {
        try {
          throw err.response.request.response;
        } catch (error) {
          throw err;
        }
      }
    },
    [AUTH_REQUEST]: async ({ commit, dispatch, rootState }, user) => {
      try {
        const response = await httpClient.post("api/users/get_auth_token/", {
          email: user.email,
          password: user.password,
        });

        const token = response.data.token;
        commit(AUTH_TOKEN, response.data);

        localStorage.setItem("user-token", token);

        await dispatch(USER_REQUEST);
        commit(DOCS_FILE_CABINET, "");
        commit(DOCS_SUCCESS, "");
        await dispatch(DOCS_REQUEST);
        commit(AUTH_AUTH, true);

        return response;
      } catch (err) {
        localStorage.removeItem("user-token");

        try {
          throw err.response.request.response;
        } catch (error) {
          throw err;
        }
      }
    },

    [AUTH_LOGOUT]: ({ commit, dispatch }) => {
      commit(AUTH_LOGOUT);

      localStorage.removeItem("user-token");
    },
  },

  mutations: {
    [AUTH_TOKEN]: (state, resp) => {
      state.token = resp.token;
    },
    [AUTH_AUTH]: (state, resp) => {
      state.auth = resp;
    },
    [AUTH_LOGOUT]: (state) => {
      state.token = "";
      state.profile = {};
      state.auth = false;
    },
  },
};
