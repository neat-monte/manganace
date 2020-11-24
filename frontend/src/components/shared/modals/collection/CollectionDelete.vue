<template>
  <a-button v-if="buttonText" type="danger" @click="showModal()">
    {{ buttonText }}
    <delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Delete collection">
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
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
    buttonText: {
      type: String,
      default: null,
    },
  },

  setup(props) {
    const router = useRouter();

    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteCollectionAsync } = useCollections();
    async function handleDelete() {
      visible.value = false;
      await deleteCollectionAsync(props.collectionId);
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