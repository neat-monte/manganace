<template>
  <section v-if="collections" id="collections">
    <div class="collections-header">
      <span class="title">Collections</span>
      <div class="controls">
        <CollectionCreate />
      </div>
    </div>

    <a-collapse :activeKey="collectionId.toString()" :bordered="false">
      <a-collapse-panel
        v-for="collection in collections"
        :key="collection.id.toString()"
        :header="collection.name"
        @click="renderImages(collection.id)"
      >
        <Collection :collection="collection" />
      </a-collapse-panel>
    </a-collapse>
  </section>
</template>

<script>
import { useRouter } from "vue-router";

import Collection from "@/components/library/Collection";
import CollectionCreate from "@/components/actions/collection/CollectionCreate";
import useCollections from "@/modules/collections";

export default {
  name: "Collections",

  props: {
    collectionId: Number,
  },

  async setup() {
    const router = useRouter();

    function renderImages(collectionId) {
      router.push({
        name: "ImagesOfCollection",
        params: { collectionId: collectionId },
      });
    }

    const { collectionsById, loadCollectionsAsync } = useCollections();

    await loadCollectionsAsync();

    return {
      collections: collectionsById,
      renderImages,
    };
  },

  components: {
    Collection,
    CollectionCreate,
  },
};
</script>

<style lang="scss" scoped>
#collections {
  display: none;
}

@include sm-desktop {
  #collections {
    display: initial;
    padding: 0 20px 10px 20px;
    height: 100%;

    .collections-header {
      display: flex;
      position: relative;
      margin: 8px 16px;

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
}
</style>