<template>
  <div></div>
  <!-- <aside v-if="loading" class="controls">
    <h1>Loading...</h1>
  </aside>

  <aside v-else class="controls">
    <h1>Controls</h1>
    <input @keyup="setSeed($event.target.value)" name="seed" placeholder="Seed" type="text" />
    <button @click="generate">Generate</button>
  </aside> -->
</template>

<script>
export default {
  name: "Controls",
};
</script>

<style lang="scss" scoped>
.controls {
  flex: 1;
  order: -1;
}

@include sm-desktop {
  .controls {
    margin-right: 10px;
  }
}

@include lg-desktop {
  .controls {
    margin-right: 20px;
  }
}
</style>