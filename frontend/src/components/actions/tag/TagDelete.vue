<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Delete tag</span>
    </template>
    <a-button type="danger" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <DeleteOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm tag delete"
    @ok="handleDelete()"
  >
    <p>
      The tag will be removed from all the images.
      <strong>It will be unrecoverable.</strong>
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import useTags from "@/modules/tags";

export default {
  name: "TagDelete",

  props: {
    tagId: Number,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteTag } = useTags();
    async function handleDelete() {
      await deleteTag(props.tagId);
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