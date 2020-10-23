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
  background: lightpink;
  display: flex;
  flex-wrap: wrap;
}

@include sm-desktop {
  #generator {
    padding: 20px $sm-generator-y-padding;
  }
}

@include lg-desktop {
  #generator {
    padding: 40px $lg-generator-y-padding;
  }
}
</style>