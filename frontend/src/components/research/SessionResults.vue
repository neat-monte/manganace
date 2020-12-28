<template>
  <a-button
    v-if="session.participant && session.progress > 0"
    type="primary"
    @click="showModal()"
  >
    Results
    <info-circle-outlined />
  </a-button>

  <a-modal v-model:visible="visible" title="Session results" :width="800">
    <Boxplot
      :data="data"
      title="Chosen multipliers for each vector of a single participant"
    />
    <ImagesList
      v-if="images"
      :images="images"
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

import { InfoCircleOutlined } from "@ant-design/icons-vue";
import Boxplot from "@/components/shared/infographics/Boxplot";
import ImagesList from "@/components/shared/image/ImagesList";

import useCollectionImages from "@/modules/collectionImages";
import useResearchData from "@/modules/researchData";

export default {
  name: "SessionResults",

  props: {
    session: { type: Object, required: true },
  },

  async setup(props) {
    const visible = ref();
    const {
      imagesByCollectionId,
      loadImagesOfCollectionAsync,
    } = useCollectionImages();
    const { getSessionResultsDataAsync } = useResearchData();

    const images = ref([]);
    const data = await getSessionResultsDataAsync(
      props.session.researchSettingId,
      props.session.id
    );

    async function showModal() {
      visible.value = !visible.value;
      await loadImagesOfCollectionAsync(props.session.participant.collectionId);
      images.value = Object.values(
        imagesByCollectionId[props.session.participant.collectionId]
      );
    }

    return {
      data,
      showModal,
      visible,
      images,
    };
  },

  components: {
    Boxplot,
    InfoCircleOutlined,
    ImagesList,
  },
};
</script>