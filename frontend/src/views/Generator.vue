<template>
  <div id="generator" class="content">
    <Suspense>
      <template #default>
        <Sessions />
      </template>
      <template #fallback>
        <Loading id="sessions" />
      </template>
    </Suspense>

    <Image />

    <Suspense>
      <template #default>
        <Controls />
      </template>
      <template #fallback>
        <Loading id="controls" />
      </template>
    </Suspense>
  </div>
</template>

<script>
import Image from "@/components/generator/Image";
import Controls from "@/components/generator/Controls";
import Sessions from "@/components/generator/Sessions";
import Loading from "@/components/shared/Loading";

export default {
  name: "Generator",
  components: {
    Image,
    Controls,
    Sessions,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#generator {
  display: flex;
  flex-flow: row wrap;

  #sessions,
  #controls,
  #generated-image {
    flex: 100%;
  }

  #generated-image {
    order: 1;
  }
}

@include tablet {
  #generator {
    #sessions,
    #controls {
      margin-bottom: 20px;
    }

    #generated-image {
      margin-bottom: 10px;
      order: initial;
    }
  }
}

@include sm-desktop {
  #generator {
    #sessions {
      flex: 0 100%;
      margin-bottom: 20px;
    }

    #controls {
      flex: 1 300px;
      margin-left: 20px;
    }

    #generated-image {
      flex: 1;
      margin-bottom: 20px;
    }
  }
}
</style>