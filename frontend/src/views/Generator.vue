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

    <Suspense>
      <template #default>
        <Activity />
      </template>
      <template #fallback>
        <Loading :replacementId="'activity'" />
      </template>
    </Suspense>
  </div>
</template>

<script>
import Image from "@/components/generator/Image";
import Controls from "@/components/generator/Controls";
import Activity from "@/components/generator/Activity";
import Loading from "@/components/shared/Loading";

export default {
  name: "Generator",
  components: {
    Image,
    Controls,
    Activity,
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
  #activity {
    flex: 100%;
  }
}

@include sm-desktop {
  #generator {
    #controls {
      flex: 1;
    }
    #generated-image {
      flex: 1;
    }
    #activity {
      flex: 0 100%;
    }
  }
}
</style>