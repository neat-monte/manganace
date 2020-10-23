<template>
  <aside class="history">
    <h1>History</h1>
  </aside>
</template>

<script>
export default {
  name: "History",
};
</script>

<style lang="scss" scoped>
.history {
  background: orange;
  min-height: 200px;

  flex: 1 100%;
}

@include sm-desktop {
  .history {
    margin-top: 10px;
  }
}

@include lg-desktop {
  .history {
    margin-top: 20px;
  }
}
</style>