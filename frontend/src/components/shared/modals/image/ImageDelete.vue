<template>
  <a-button v-if="buttonText" type="danger" @click="showModal()">
    {{ buttonText }}
    <delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Delete image">
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
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
import useCollectionImages from "@/modules/collectionImages";

export default {
  name: "ImageDelete",

  props: {
    imageId: Number,
    buttonText: {
      type: String,
      default: null,
    },
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteCollectionImageAsync } = useCollectionImages();
    async function handleDelete() {
      visible.value = false;
      await deleteCollectionImageAsync(props.imageId);
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