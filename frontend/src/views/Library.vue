<template>
  <div id="library" class="content">
    <div v-if="error">{{ error }}</div>

    <Suspense>
      <template #default>
        <Collections :collectionId="collectionId" />
      </template>
      <template #fallback>
        <Loading />
      </template>
    </Suspense>

    <Suspense>
      <template #default>
        <Images :collectionId="collectionId" />
      </template>
      <template #fallback>
        <Loading />
      </template>
    </Suspense>
  </div>
</template>

<script>
import { computed, ref, onErrorCaptured, watchEffect } from "vue";
import { useRoute } from "vue-router";
import Collections from "@/components/library/Collections";
import Images from "@/components/library/Images";
import Loading from "@/components/shared/Loading";

export default {
  name: "Library",

  setup() {
    const route = useRoute();
    watchEffect(() => route.params);

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
</style>