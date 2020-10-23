<template>
  <header class="header">
    <div class="brand">
      <router-link to="/">
        <h1>Manganace</h1>
      </router-link>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header",
};
</script>

<style lang="scss" scoped>
.header {
  grid-area: header;
  height: $header-height;
  background: tomato;
}
</style>