<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Save image</span>
    </template>
    <a-button
      @click="showModal()"
      :disabled="!image.seed || !image.filename"
      type="primary"
      shape="circle"
    >
      <template v-slot:icon>
        <SaveOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal v-model:visible="visible" title="Save image" @ok="handleSave()">
    <a-form>
      <a-form-item label="Collection">
        <Suspense>
          <template #default>
            <CollectionSelect @collection-id-set="setCollectionId" />
          </template>
        </Suspense>
      </a-form-item>
      <a-form-item label="Description">
        <a-textarea
          v-model:value="newImage.description"
          placeholder="Give picture a short description"
          :rows="2"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref, watchEffect } from "vue";
import { SaveOutlined } from "@ant-design/icons-vue";

import CollectionSelect from "@/components/actions/collection/CollectionSelect";
import notification from "@/services/notification";
import useImages from "@/modules/useImages";
import useGenerator from "@/modules/useGenerator";

export default {
  name: "ImageSave",

  setup() {
    const { image } = useGenerator();

    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { createImage } = useImages();
    const newImage = reactive({
      description: null,
      collectionId: null,
      imageTags: [],
    });

    watchEffect(() => {
      newImage.seed = image.seed;
      newImage.filename = image.filename;
    });

    function setCollectionId(id) {
      newImage.collectionId = id;
    }

    async function handleSave() {
      const created = await createImage(newImage);
      visible.value = false;
      notification.images.added(created);
    }

    return {
      image,
      setCollectionId,
      newImage,
      handleSave,
      showModal,
      visible,
    };
  },

  components: { SaveOutlined, CollectionSelect },
};
</script>