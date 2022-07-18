// import { AUTH_LOGOUT } from "@/store/mutation-types";
import axios from "axios";

const httpClient = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_HOST + "/",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Token " + localStorage.getItem("user-token"),
  },
});

// Обработка ошибок с бэка
httpClient.interceptors.response.use(undefined, async (err) => {
  if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
    throw err.response.data;
    // this.$store.dispatch(AUTH_LOGOUT);
  }

  throw err;
});

export default httpClient;
