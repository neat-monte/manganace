<template>
  <a-button
    v-if="session.participant && session.progress > 0"
    type="primary"
    @click="showModal()"
  >
    Results
    <info-circle-outlined />
  </a-button>

  <a-modal
    v-model:visible="visible"
    title="Session results"
    @ok="handleCreate()"
  >
    <ImagesList v-if="images" :images="images" :allowDelete="false" />

    <template #footer>
      <a-button key="submit" @click="showModal()">OK</a-button>
    </template>
  </a-modal>
</template>

<script>
import { ref } from "vue";

import { InfoCircleOutlined } from "@ant-design/icons-vue";
import ImagesList from "@/components/shared/ImagesList";

import useImages from "@/modules/images";

export default {
  name: "SessionResults",

  props: {
    session: Object,
  },

  setup(props) {
    const visible = ref();
    const { imagesByCollectionId, loadImagesOfCollectionAsync } = useImages();

    const images = ref([]);

    async function showModal() {
      visible.value = !visible.value;
      await loadImagesOfCollectionAsync(props.session.participant.collectionId);
      images.value = Object.values(
        imagesByCollectionId[props.session.participant.collectionId]
      );
    }

    return {
      showModal,
      visible,
      images,
    };
  },

  components: {
    InfoCircleOutlined,
    ImagesList,
  },
};
</script>