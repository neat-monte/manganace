<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Delete collection</span>
    </template>
    <a-button type="danger" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <DeleteOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm collection delete"
    @ok="handleDelete()"
  >
    <p>
      The collection will be removed with all the data.
      <strong>It will be unrecoverable.</strong>
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { DeleteOutlined } from "@ant-design/icons-vue";
import useCollections from "@/modules/collections";

export default {
  name: "CollectionDelete",

  props: {
    collectionId: Number,
  },

  setup(props) {
    const router = useRouter();

    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteCollectionAsync } = useCollections();
    async function handleDelete() {
      await deleteCollectionAsync(props.collectionId);
      visible.value = false;
      router.push({ name: "Collections" });
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