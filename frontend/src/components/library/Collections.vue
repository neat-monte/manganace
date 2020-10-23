<template>
  <div v-if="collections" class="collections">
    <div class="collections-header">
      <h2>Collections</h2>
      <div class="collections-controls">
        <CreateCollection />
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
import CreateCollection from "@/components/library/CreateCollection";
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
    CreateCollection,
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
    flex: 1 30%;
    background: lightcoral;

    .collections-header {
      display: flex;

      h2 {
        flex: 1 80%;
        margin: 0;
        padding: 10px;
      }

      .collections-controls {
        flex: 1 20%;
        align-self: center;
      }
    }
  }
}
</style>