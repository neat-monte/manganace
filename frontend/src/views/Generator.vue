<template>
  <div id="generator" class="content">
    <Image />
    <Controls />
    <History />
  </div>
</template>

<script>
import Image from "@/components/generator/Image";
import Controls from "@/components/generator/Controls";
import History from "@/components/generator/History";

export default {
  name: "Generator",
  components: {
    Image,
    Controls,
    History,
  },
};
</script>

<style lang="scss" scoped>
#generator {
  display: flex;
  flex-wrap: wrap;
}
</style>