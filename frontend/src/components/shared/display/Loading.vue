/**
 * Idea source: https://loading.io/css/
 */

<template>
  <div class="loading">
    <div class="dual-ring"></div>
  </div>
</template>

<script>
export default {
  name: "Loading",
};
</script>

<style lang="scss" scoped>
.loading {
  flex: 1;
  align-self: center;
  width: 100%;
  height: 100%;
  position: relative;

  .dual-ring {
    width: 36px;
    height: 36px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    &:after {
      content: " ";
      display: block;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 2px solid #fff;
      border-color: $primary transparent $primary transparent;
      animation: dual-ring 1.2s linear infinite;
    }
  }

  @keyframes dual-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
}
</style>