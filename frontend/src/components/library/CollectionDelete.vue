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
    <p>
      The collection will be removed with all the data. It will be
      unrecoverable.
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import { notification } from "ant-design-vue";
import useCollections from "@/modules/useCollections";

export default {
  name: "CollectionUpdate",

  props: {
    collectionId: Number,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteCollection } = useCollections();
    async function handleDelete() {
      const deleted = await deleteCollection(props.collectionId);
      visible.value = false;
      notification.open({
        message: "Collection deleted",
        description: `Collection "${deleted.name}" was deleted successfully`,
        placement: "bottomRight",
      });
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