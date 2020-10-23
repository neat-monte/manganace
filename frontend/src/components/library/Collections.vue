<template>
  <div v-if="collections" class="collections">
    <div class="collections-header">
      <h2>Collections</h2>
      <div class="collections-controls">
        <Button shape="circle">
          <PlusOutlined />
        </Button>
      </div>
    </div>

    <a-collapse :activeKey="collectionId.toString()" :bordered="false">
      <a-collapse-panel
        v-for="collection in collections"
        :key="collection.id.toString()"
        :header="collection.name"
        v-on:click="renderImages(collection.id)"
      >
        <Collection :collection="collection" />
      </a-collapse-panel>
    </a-collapse>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { PlusOutlined } from "@ant-design/icons-vue";
import Collection from "@/components/library/Collection";
import Button from "@/components/shared/Button";
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
    Button,
    PlusOutlined,
  },
};
</script>