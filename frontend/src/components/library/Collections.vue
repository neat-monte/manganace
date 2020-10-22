<template>
  <div v-if="collections" id="collections">
    <Collection
      v-for="collection in collections"
      :key="collection.id"
      :collection="collection"
    />
  </div>
</template>
<script>
import Collection from "@/components/library/Collection";
import useCollections from "@/modules/useCollections";

export default {
  name: "Collections",

  async setup() {
    const { state, loadCollections } = useCollections();
    await loadCollections();
    return {
      collections: state.collections,
    };
  },

  components: {
    Collection,
  },
};
</script>