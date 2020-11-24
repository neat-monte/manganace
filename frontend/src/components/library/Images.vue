<template>
  <a-button type="primary" @click="showModal()">
    Images
    <picture-outlined />
  </a-button>

  <a-modal
    v-model:visible="visible"
    :title="`Collection images (${images.length})`"
    :width="800"
  >
    <ImagesList
      :images="images"
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
import ImagesList from "@/components/shared/ImagesList";

import useImages from "@/modules/images";

export default {
  name: "SessionResults",

  props: {
    collectionId: { type: Number, required: true },
  },

  setup(props) {
    const visible = ref();
    const { imagesByCollectionId, loadImagesOfCollectionAsync } = useImages();

    const images = ref([]);

    async function showModal() {
      visible.value = !visible.value;
      await loadImagesOfCollectionAsync(props.collectionId);
      images.value = Object.values(imagesByCollectionId[props.collectionId]);
    }

    return {
      showModal,
      visible,
      images,
    };
  },

  components: {
    PictureOutlined,
    ImagesList,
  },
};
</script>