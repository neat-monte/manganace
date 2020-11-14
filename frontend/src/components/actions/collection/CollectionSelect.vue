<template>
  <div class="collection-select">
    <a-auto-complete
      :data-source="dropdownOptions"
      placeholder="Select collection"
      @search="onSearch"
      @select="onSelectOrChange"
      @change="onSelectOrChange"
      class="autocomplete-input"
    />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import useCollections from "@/modules/collections";

export default {
  name: "CollectionSelect",

  emits: ["collection-id-set"],

  async setup(_, context) {
    const { collectionsById, loadCollectionsAsync } = useCollections();

    const collectionsOptions = ref([]);
    const dropdownOptions = ref([]);
    const selectedCollection = ref(null);

    watchEffect(() => {
      collectionsOptions.value = [];
      for (const [id, collection] of Object.entries(collectionsById)) {
        collectionsOptions.value.push({
          value: id.toString(),
          text: collection.name,
        });
      }
      if (!selectedCollection.value) {
        dropdownOptions.value = collectionsOptions.value;
      }
    });

    function onSearch(searchText) {
      dropdownOptions.value = !searchText
        ? collectionsOptions.value
        : collectionsOptions.value.filter((opt) =>
            opt.text.toLowerCase().includes(searchText.toLowerCase())
          );
    }

    function onSelectOrChange(value) {
      const any = collectionsOptions.value.filter((opt) => opt.value === value);
      if (any.length > 0) {
        selectedCollection.value = value;
        context.emit("collection-id-set", value);
      } else {
        selectedCollection.value = null;
      }
    }

    await loadCollectionsAsync();

    return {
      onSearch,
      onSelectOrChange,
      dropdownOptions,
      selectedCollection,
    };
  },
};
</script>

<style lang="scss" scoped>
.collection-select {
  display: flex;
  width: 100%;

  .autocomplete-input {
    width: 100%;
  }
}
</style>