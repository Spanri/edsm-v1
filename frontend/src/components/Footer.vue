<template>
  <div class="footer-wrapper">
    <div class="footer">
      МТУСИ, 2019 - 2022 |
      <label class="footer__link" @click="goToHelp()">Помощь</label>
    </div>
  </div>
</template>

<script>
export default {
  name: "Footer",

  methods: {
    goToHelp() {
      this.$router.push("/help");
    },
  },
};
</script>

<style lang="scss" scoped>
.footer {
  width: 100%;
  max-width: 1400px;
  text-align: center;
  margin: 0 8px 8px;
  color: white;

  &-wrapper {
    background-color: #347090;
    height: 40px;
  }

  &__link {
    color: white;
    text-decoration: none;
    text-decoration: underline;

    &:hover {
      cursor: pointer;
      color: #aaa9f8;
    }
  }
}
</style>
