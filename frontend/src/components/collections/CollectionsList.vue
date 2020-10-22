<template>
  <div v-if="collections" class="collections-list">
    <AsyncCollectionCard
      v-for="collection in collections"
      :key="collection.id"
      v-bind:collectionId="collection.id"
    />
  </div>
</template>

<script>
import { defineAsyncComponent } from "vue";
import useLibrary from "@/modules/useLibrary";
import Loading from "@/components/Loading";

const AsyncCollectionCard = defineAsyncComponent({
  loader: () => import("@/components/collections/CollectionCard"),
  loadingComponent: Loading,
  delay: 200,
  suspensible: false,
});

export default {
  name: "CollectionsList",
  async setup() {
    const { state, loadCollections } = useLibrary();
    await loadCollections();
    return {
      collections: state.collections,
      images: state.images,
    };
  },
  components: {
    AsyncCollectionCard,
  },
};
</script>