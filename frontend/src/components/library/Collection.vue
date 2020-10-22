<template>
  <div class="collection">
    <h2>{{ collection.name }}</h2>
  </div>
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