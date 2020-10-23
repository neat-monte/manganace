<template>
  <a-button class="button" :shape="shape">
    <template v-slot:icon>
      <slot />
    </template>
    {{ text }}
  </a-button>
</template>

<script>
export default {
  name: "Button",

  props: {
    shape: String,
    text: String,
    event: Function,
  },
};
</script>

<style lang="scss" scoped>
.button {
  background-color: skyblue;
}
</style>