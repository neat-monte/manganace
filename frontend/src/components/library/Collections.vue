<template>
  <section id="collections">
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

    <Empty v-if="collections.length == 0" />
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";
import { useRouter } from "vue-router";

import Collection from "@/components/library/Collection";
import CollectionCreate from "@/components/actions/collection/CollectionCreate";
import Empty from "@/components/shared/Empty";

import useCollections from "@/modules/collections";

export default {
  name: "Collections",

  props: {
    collectionId: Number,
  },

  async setup(props) {
    const router = useRouter();
    const { collectionsById, loadCollectionsAsync } = useCollections();
    const collections = ref([]);

    watchEffect(() => {
      if (
        props.collectionId &&
        collectionsById &&
        !(props.collectionId in collectionsById)
      ) {
        router.push({
          name: "NotFound",
        });
      }

      collections.value = Object.values(collectionsById);
    });

    function renderImages(collectionId) {
      router.push({
        name: "CollectionImages",
        params: { collectionId: collectionId },
      });
    }

    await loadCollectionsAsync();

    return {
      collections,
      renderImages,
    };
  },

  components: {
    Collection,
    CollectionCreate,
    Empty,
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