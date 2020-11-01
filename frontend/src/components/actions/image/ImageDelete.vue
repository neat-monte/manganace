<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Delete image</span>
    </template>
    <a-button type="danger" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <DeleteOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm image delete"
    @ok="handleDelete()"
  >
    <p>The image will be removed. <strong>It will be unrecoverable.</strong></p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
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
      await deleteImage(props.imageId);
      visible.value = false;
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