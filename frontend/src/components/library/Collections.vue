<template>
  <section id="collections">
    <div class="collections-header">
      <span class="title">Collections</span>
      <div class="controls">
        <CollectionCreate buttonText="Create" />
      </div>
    </div>
    <a-list
      :grid="{ gutter: 20, xs: 1, sm: 2, md: 1, lg: 2, xl: 3, xxl: 4 }"
      :data-source="collections"
    >
      <template #renderItem="{ item, index }">
        <a-list-item :key="index">
          <CollectionCard :collection="item" />
        </a-list-item>
      </template>
    </a-list>
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";

import CollectionCard from "@/components/library/CollectionCard";
import CollectionCreate from "@/components/shared/modals/collection/CollectionCreate";

import useCollections from "@/modules/collections";

export default {
  name: "Collections",

  async setup() {
    const { collectionsById, loadCollectionsAsync } = useCollections();
    const collections = ref([]);

    watchEffect(() => {
      collections.value = Object.values(collectionsById);
    });

    await loadCollectionsAsync();

    return {
      collections,
    };
  },

  components: {
    CollectionCreate,
    CollectionCard,
  },
};
</script>

<style lang="scss" scoped>
#collections {
  display: initial;
  padding: 0 20px 10px 20px;
  height: 100%;

  .collections-header {
    display: flex;
    position: relative;
    margin: 8px 0;

    .title {
      width: 100%;
      margin: 0;
      padding: 10px;
    }

    .controls {
      position: absolute;
      align-self: center;
      right: 0;
    }
  }
}

@include tablet {
  #collections {
    padding: 0 0 10px 20px;
  }
}
</style>