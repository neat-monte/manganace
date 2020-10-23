<template>
  <div class="collection"></div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Collection",
  props: {
    collection: Object,
  },
  setup() {
    const isExpanded = ref();

    return {
      isExpanded,
    };
  },
};
</script>

<style lang="scss" scoped>
.collection {
  height: 80px;
  border-top: 1px solid black;
  border-bottom: 1px solid black;
  margin-bottom: 10px;
  cursor: pointer;
}
</style>