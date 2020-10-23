<template>
  <div class="collection">
    <h3>{{ collection.name }}</h3>
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