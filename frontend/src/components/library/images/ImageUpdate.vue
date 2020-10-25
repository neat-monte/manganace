<template>
  <a-button type="primary" shape="circle" @click="showModal()">
    <template v-slot:icon>
      <EditOutlined />
    </template>
  </a-button>

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
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import notification from "@/services/notification";
import useImages from "@/modules/useImages";

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

    const { updateImage } = useImages();
    const updatedImage = reactive({
      id: props.image.id,
      description: props.image.description,
      collectionId: props.image.collectionId,
    });
    async function handleUpdate() {
      const updated = await updateImage(updatedImage);
      visible.value = false;
      notification.images.updated(updated);
    }

    return {
      updatedImage,
      handleUpdate,
      showModal,
      visible,
    };
  },

  components: { EditOutlined },
};
</script>