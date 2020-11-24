<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Save image</span>
    </template>
    <a-button
      @click="showModal()"
      :disabled="!currentImage.seed"
      type="primary"
    >
      <template v-slot:icon>
        <save-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal v-model:visible="visible" title="Save image" @ok="handleSave()">
    <a-form>
      <a-form-item label="Collection">
        <Suspense>
          <template #default>
            <CollectionSelect v-model="newImage.collectionId" />
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
      <a-form-item label="Tags">
        <Suspense>
          <template #default>
            <TagSelect v-model="newImage.tagsIds" />
          </template>
        </Suspense>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref, watchEffect } from "vue";
import { SaveOutlined } from "@ant-design/icons-vue";

import CollectionSelect from "@/components/actions/collection/CollectionSelect";
import TagSelect from "@/components/actions/tag/TagSelect";
import useImages from "@/modules/images";
import useGenerator from "@/modules/generator";

export default {
  name: "ImageSave",

  setup() {
    const { currentImage } = useGenerator();

    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { addImageAsync } = useImages();
    const newImage = reactive({
      description: null,
      collectionId: null,
      tagsIds: [],
    });

    watchEffect(() => {
      newImage.imageId = currentImage.id;
    });

    async function handleSave() {
      await addImageAsync(newImage);
      visible.value = false;
    }

    return {
      currentImage,
      newImage,
      handleSave,
      showModal,
      visible,
    };
  },

  components: {
    SaveOutlined,
    CollectionSelect,
    TagSelect,
  },
};
</script>