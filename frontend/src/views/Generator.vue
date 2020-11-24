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

    <Image v-if="currentSession.id" />

    <Suspense v-if="currentSession.id">
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
import Loading from "@/components/shared/display/Loading";
import useGenerator from "@/modules/generator";

export default {
  name: "Generator",

  setup() {
    const { currentSession } = useGenerator();

    return {
      currentSession,
    };
  },

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
    #controls,
    #generated-image {
      margin-bottom: 20px;
    }
  }
}

@include sm-desktop {
  #generator {
    #sessions {
      flex: 100%;
    }

    #controls {
      flex: 1 300px;
      margin-left: 20px;
    }

    #generated-image {
      flex: 0;
      order: initial;
    }
  }
}
</style>