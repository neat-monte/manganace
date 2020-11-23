<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Edit image</span>
    </template>
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <edit-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Edit image description"
    @ok="handleUpdate()"
  >
    <a-form>
      <a-form-item label="Description">
        <a-textarea
          v-model:value="updatedImage.description"
          placeholder="Give picture a short description"
          :rows="2"
        />
      </a-form-item>

      <a-form-item label="Tags">
        <Suspense>
          <template #default>
            <TagSelect v-model="updatedImage.tagsIds" />
          </template>
        </Suspense>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import TagSelect from "@/components/actions/tag/TagSelect";
import useImages from "@/modules/images";

export default {
  name: "ImageUpdate",

  props: {
    image: Object,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { updateImageAsync } = useImages();
    const updatedImage = reactive({
      id: props.image.id,
      description: props.image.description,
      collectionId: props.image.collectionId,
      tagsIds: props.image.tagsIds,
    });

    async function handleUpdate() {
      await updateImageAsync(updatedImage);
      visible.value = false;
    }

    return {
      updatedImage,
      handleUpdate,
      showModal,
      visible,
    };
  },

  components: {
    EditOutlined,
    TagSelect,
  },
};
</script>