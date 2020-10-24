<template>
  <a-button type="primary" shape="circle" @click="showModal()">
    <template v-slot:icon>
      <PlusOutlined />
    </template>
  </a-button>

  <a-modal
    v-model:visible="visible"
    title="Create new collection"
    @ok="handleCreate()"
  >
    <a-input v-model:value="newCollection.name" placeholder="Name" />

    <a-textarea
      v-model:value="newCollection.description"
      placeholder="Description"
      :rows="4"
    />
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";
import notification from "@/services/notification";
import useCollections from "@/modules/useCollections";

export default {
  name: "CollectionCreate",

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { addCollection } = useCollections();
    const newCollection = reactive({
      name: null,
      description: null,
    });
    async function handleCreate() {
      const created = await addCollection(newCollection);
      visible.value = false;
      notification.collections.created(created);
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