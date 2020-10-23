<template>
  <div class="loading">
    <span>Loading</span>
  </div>
</template>

<script>
export default {
  name: "Loading",
};
</script>

<style lang="scss" scoped>
.loading {
  display: flex;
  justify-content: center;
  align-content: center;

  height: 100%;

  span {
    height: 20px;
    animation: spin 2s linear infinite;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>