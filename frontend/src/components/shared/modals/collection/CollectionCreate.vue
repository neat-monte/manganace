<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <plus-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Create new collection">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <plus-outlined />
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

  props: {
    buttonText: {
      type: String,
      default: null,
    },
  },

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { createCollectionAsync } = useCollections();
    const newCollection = reactive({
      name: null,
      description: null,
    });
    async function handleCreate() {
      visible.value = false;
      await createCollectionAsync(newCollection);
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