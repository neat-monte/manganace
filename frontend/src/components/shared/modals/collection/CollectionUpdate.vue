<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <edit-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Edit collection">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <edit-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Edit collection"
    @ok="handleUpdate()"
  >
    <a-form>
      <a-form-item label="Name">
        <a-input
          v-model:value="updatedCollection.name"
          placeholder="Well describing name"
        />
      </a-form-item>
      <a-form-item label="Description">
        <a-textarea
          v-model:value="updatedCollection.description"
          placeholder="What does this collection contain?"
          :rows="2"
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import useCollections from "@/modules/collections";

export default {
  name: "CollectionUpdate",

  props: {
    collection: Object,
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

    const { updateCollectionAsync } = useCollections();
    const updatedCollection = reactive({
      id: props.collection.id,
      name: props.collection.name,
      description: props.collection.description,
    });
    async function handleUpdate() {
      visible.value = false;
      await updateCollectionAsync(updatedCollection);
    }

    return {
      updatedCollection,
      handleUpdate,
      showModal,
      visible,
    };
  },

  components: { EditOutlined },
};
</script>