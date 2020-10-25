<template>
  <div id="generator" class="content">
    <Image />

    <Suspense>
      <template #default>
        <Controls />
      </template>
      <template #fallback>
        <Loading :replacementId="'controls'" />
      </template>
    </Suspense>

    <History />
  </div>
</template>

<script>
import Image from "@/components/generator/Image";
import Controls from "@/components/generator/Controls";
import History from "@/components/generator/History";
import Loading from "@/components/shared/Loading";

export default {
  name: "Generator",
  components: {
    Image,
    Controls,
    History,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#generator {
  display: flex;
  flex-wrap: wrap;

  #controls {
    order: -1;
  }
}
</style>