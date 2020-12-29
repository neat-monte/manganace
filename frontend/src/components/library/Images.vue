<template>
  <a-button type="primary" @click="showModal()">
    Images
    <picture-outlined />
  </a-button>

  <a-modal
    v-model:visible="visible"
    :title="`${collection.name} (${imagesByCollectionId[collectionId]?.length})`"
    :width="800"
  >
    <ImagesList
      :images="imagesByCollectionId[collectionId] ?? []"
      :allowDelete="true"
      :allowUpdate="true"
      :allowDownload="true"
    />
    <template #footer>
      <a-button key="submit" @click="showModal()">OK</a-button>
    </template>
  </a-modal>
</template>

<script>
import { ref } from "vue";

import { PictureOutlined } from "@ant-design/icons-vue";
import ImagesList from "@/components/shared/image/ImagesList";

import useCollectionImages from "@/modules/collectionImages";
import useCollections from "@/modules/collections";

export default {
  name: "SessionResults",

  props: {
    collectionId: { type: Number, required: true },
  },

  setup(props) {
    const visible = ref();
    const {
      imagesByCollectionId,
      loadImagesOfCollectionAsync,
    } = useCollectionImages();

    const { collectionsById } = useCollections();
    const collection = collectionsById[props.collectionId];

    async function showModal() {
      visible.value = !visible.value;
      await loadImagesOfCollectionAsync(props.collectionId);
    }

    return {
      showModal,
      visible,
      imagesByCollectionId,
      collection,
    };
  },

  components: {
    PictureOutlined,
    ImagesList,
  },
};
</script>