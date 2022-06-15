<template>
  <div class="app">
    <Auth v-if="!isAuthenticated" />

    <div v-else-if="isSystemLoading" class="app__load">
      <p class="app__load-text">
        Система <br />
        загружается
      </p>

      <svg
        class="loadSvg"
        version="1.1"
        viewBox="0 0 16 16"
        xml:space="preserve"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
      >
        <path
          d="M14,8c-0.609,0-0.898,0.43-1,0.883C12.635,10.516,11.084,13,8,13c-0.757,0-1.473-0.172-2.114-0.474L6.414,12  C6.773,11.656,7,11.445,7,11c0-0.523-0.438-1-1-1H3c-0.609,0-1,0.492-1,1v3c0,0.541,0.428,1,1,1c0.484,0,0.688-0.273,1-0.594  l0.408-0.407C5.458,14.632,6.685,15,8,15c4.99,0,7-4.75,7-5.938C15,8.336,14.469,8,14,8z M3,7.117C3.365,5.485,4.916,3,8,3  c0.757,0,1.473,0.171,2.114,0.473L9.586,4C9.227,4.344,9,4.555,9,5c0,0.523,0.438,1,1,1h3c0.609,0,1-0.492,1-1V2  c0-0.541-0.428-1-1-1c-0.484,0-0.688,0.273-1,0.594l-0.408,0.407C10.542,1.368,9.315,1,8,1C3.01,1,1,5.75,1,6.938  C1,7.664,1.531,8,2,8C2.609,8,2.898,7.57,3,7.117z"
        />
      </svg>
    </div>

    <div v-else class="app__authenticated">
      <Header />
      <router-view />
      <Footer />
    </div>
  </div>
</template>

<script>
import { AUTH_LOGOUT } from "@/store/mutation-types";
import axios from "axios";

export default {
  name: "App",

  components: {
    Auth: () => import("@/views/Auth"),
    Header: () => import("@/components/Header"),
    Footer: () => import("@/components/Footer"),
  },

  computed: {
    /**
     * Юзер авторизован?
     */
    isAuthenticated() {
      return this.$store.getters.isAuthenticated || this.$store.getters.auth;
    },

    /**
     * Система загружается?
     */
    isSystemLoading() {
      return this.isAuthenticated && !this.$store.getters.auth;
    },
  },

  created: function () {
    // Обработка ошибок с бэка
    axios.interceptors.response.use(undefined, async (err) => {
      if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
        this.$store.dispatch(AUTH_LOGOUT);
      }

      throw err;
    });
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=El+Messiri:600|Roboto:300|Spectral|Roboto|PT+Sans+Narrow&display=swap");

html {
  font-family: "Roboto", serif;
  font-weight: 500;

  width: 100%;
  min-height: 100%;
}

body {
  width: 100%;
  height: 100vh;
}

*:not(svg):hover {
  transition: all 0.2s;
}

router-view {
  overflow-y: auto;
  height: 100vh;
}

@media (max-width: 500px) {
  * {
    font-size: 14px;
  }
}

/* Для всего проекта */
button:not(.showPassword),
.button {
  border: 0;
  padding: 8px;
  margin-top: 15px;
  margin-bottom: 0px;
  margin-right: 7px;
  color: white;
  font-family: "Courier New", Courier, monospace;
  font-size: 14px;
  background-color: #347090;
  box-shadow: 0 3px rgba(170, 169, 248, 1);
  transform: translate(0, -3px);
  box-shadow: 0 5px 0px 0px rgba(170, 169, 248, 1);
}

button:active,
a:active {
  box-shadow: none;
  transform: translate(0px, 0px);
}

button:hover {
  cursor: pointer;
}

input[type="checkbox"] {
  height: 15px;
}

input {
  border: 0;
  height: 30px;
  margin: 0 auto;
  padding-left: 15px;
  padding-right: 15px;
}
</style>

<style lang="scss" scoped>
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.app {
  width: 100%;
  height: 100%;

  &__load {
    display: grid;
    grid-template-rows: auto max-content auto;

    height: 100vh;
    width: 100vw;
    margin: 0 auto;
    background: #64b2db;
    padding: 10px;

    &-text {
      color: white;
      padding: 0px;
      text-align: center;
    }

    &-svg {
      fill: white;
      enable-background: new 0 0 16 16;
      padding: 15px;
      margin-left: 15px;
      height: 30px;
      width: 30px;
      animation: spin 3s linear infinite;
    }
  }

  &__authenticated {
    height: 100vh;
    width: calc(100vw - 15px);
    display: grid;
    grid-template-rows: max-content auto max-content;
  }
}
</style>
