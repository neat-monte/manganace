<template>
  <div v-if="collections" class="collections">
    <div class="collections-header">
      <h1 class="title">Collections</h1>
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
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import Collection from "@/components/library/Collection";
import CollectionCreate from "@/components/library/CollectionCreate";
import useCollections from "@/modules/useCollections";

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

    const { state, loadCollections } = useCollections();

    await loadCollections();

    return {
      collections: state.collections,
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
.collections {
  display: none;
}

@include sm-desktop {
  .collections {
    display: block;
    background: lightcoral;

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