/**
 * Source: https://loading.io/css/
 */

<template>
  <div :id="replacementId" class="loading">
    <div class="dual-ring"></div>
  </div>
</template>

<script>
export default {
  name: "Loading",

  props: {
    replacementId: String,
  },
};
</script>

<style lang="scss" scoped>
.loading {
  flex: 1;
  align-self: center;
  width: 100%;

  .dual-ring {
    display: inline-block;
    width: 80px;
    height: 80px;

    &:after {
      content: " ";
      display: block;
      width: 48px;
      height: 48px;
      margin: 12px;
      border-radius: 50%;
      border: 6px solid #fff;
      border-color: $primary transparent $primary transparent;
      animation: dual-ring 1.2s linear infinite;
    }
  }

  @keyframes dual-ring {
    0% {
      transform: rotate(0deg);
    }
    50% {
      transform: rotate(180deg);
      width: 64px;
      height: 64px;
      margin: 8px;
    }
    100% {
      transform: rotate(360deg);
    }
  }
}
</style>