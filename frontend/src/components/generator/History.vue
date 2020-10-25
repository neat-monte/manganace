<template>
  <section class="history">
    <span class="title">History</span>
  </section>
</template>

<script>
export default {
  name: "History",
};
</script>

<style lang="scss" scoped>
.history {
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