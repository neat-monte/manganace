<template>
  <a-button type="danger" shape="circle" @click="showModal()">
    <template v-slot:icon>
      <DeleteOutlined />
    </template>
  </a-button>

  <a-modal
    v-model:visible="visible"
    title="Confirm delete"
    @ok="handleDelete()"
  >
    <p>The image will be removed. It will be unrecoverable.</p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import notification from "@/services/notification";
import useImages from "@/modules/useImages";

export default {
  name: "ImageDelete",

  props: {
    imageId: Number,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteImage } = useImages();
    async function handleDelete() {
      const deleted = await deleteImage(props.imageId);
      visible.value = false;
      notification.images.deleted(deleted);
    }

    return {
      handleDelete,
      showModal,
      visible,
    };
  },

  components: { DeleteOutlined },
};
</script>