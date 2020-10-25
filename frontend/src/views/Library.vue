<template>
  <div id="library" class="content">
    <Suspense>
      <template #default>
        <Collections :collectionId="collectionId" />
      </template>
      <template #fallback>
        <Loading :replacementId="'collections'" />
      </template>
    </Suspense>

    <Suspense>
      <template #default>
        <Images :collectionId="collectionId" />
      </template>
      <template #fallback>
        <Loading :replacementId="'images'" />
      </template>
    </Suspense>
  </div>
</template>

<script>
import { computed, ref, onErrorCaptured } from "vue";
import { useRoute } from "vue-router";
import Collections from "@/components/library/Collections";
import Images from "@/components/library/Images";
import Loading from "@/components/shared/Loading";

export default {
  name: "Library",

  setup() {
    const route = useRoute();

    const collectionId = computed(() => Number(route.params.collectionId));

    const error = ref(null);
    onErrorCaptured((e) => {
      error.value = e;
    });

    return {
      error,
      collectionId,
    };
  },

  components: {
    Collections,
    Images,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#library {
  display: flex;
  flex-wrap: wrap;
}

@include sm-desktop {
  #library {
    #collections {
      flex: 0 300px;
    }

    #images {
      flex: 1;
    }
  }
}
</style>