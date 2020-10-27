<template>
  <div id="generator" class="content">
    <Suspense>
      <template #default>
        <Controls />
      </template>
      <template #fallback>
        <Loading :replacementId="'controls'" />
      </template>
    </Suspense>
    <Image />
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
  flex-flow: row wrap;

  #controls,
  #generated-image,
  #history {
    flex: 100%;
  }
}

@include sm-desktop {
  #generator {
    #controls {
      flex: 1 300px;
    }
    #generated-image {
      flex: 1 512px;
    }
    #history {
      flex: 1 100%;
    }
  }
}
</style>