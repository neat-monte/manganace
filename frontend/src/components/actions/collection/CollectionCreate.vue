<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Create new collection</span>
    </template>
    <a-button type="primary" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <PlusOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Create new collection"
    @ok="handleCreate()"
  >
    <a-form>
      <a-form-item label="Name">
        <a-input
          v-model:value="newCollection.name"
          placeholder="Well describing name"
        />
      </a-form-item>
      <a-form-item label="Description">
        <a-textarea
          v-model:value="newCollection.description"
          placeholder="What does this collection contain?"
          :rows="2"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";
import useCollections from "@/modules/collections";

export default {
  name: "CollectionCreate",

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { addCollectionAsync } = useCollections();
    const newCollection = reactive({
      name: null,
      description: null,
    });
    async function handleCreate() {
      await addCollectionAsync(newCollection);
      visible.value = false;
    }

    return {
      newCollection,
      handleCreate,
      showModal,
      visible,
    };
  },

  components: { PlusOutlined },
};
</script>