<template>
  <a-button type="primary" shape="circle" @click="showModal()">
    <template v-slot:icon>
      <EditOutlined />
    </template>
  </a-button>

  <a-modal
    v-model:visible="visible"
    title="Edit collection"
    @ok="handleUpdate()"
  >
    <a-input v-model:value="updatedCollection.name" placeholder="Name" />

    <a-textarea
      v-model:value="updatedCollection.description"
      placeholder="Description"
      :rows="4"
    />

    <a-checkbox v-model:checked="updatedCollection.isArchived">
      Archive this collection
    </a-checkbox>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import { notification } from "ant-design-vue";
import useCollections from "@/modules/useCollections";

export default {
  name: "CollectionUpdate",

  props: {
    collection: Object,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { updateCollection } = useCollections();
    const updatedCollection = reactive({
      id: props.collection.id,
      name: props.collection.name,
      description: props.collection.description,
      isArchived: props.collection.isArchived,
    });
    async function handleUpdate() {
      const updated = await updateCollection(updatedCollection);
      visible.value = false;
      notification.open({
        message: "Collection updated",
        description: `Collection "${updated.name}" was updated successfully`,
        placement: "bottomRight",
      });
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