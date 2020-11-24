<template>
  <a-empty :image="simpleImage" class="ant-empty-normal" />
</template>

<script>
import { Empty } from "ant-design-vue";

export default {
  name: "Empty",

  setup() {
    const simpleImage = Empty.PRESENTED_IMAGE_SIMPLE;

    return {
      simpleImage,
    };
  },
};
</script>