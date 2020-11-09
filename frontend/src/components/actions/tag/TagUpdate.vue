<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Edit tag</span>
    </template>
    <a-button type="primary" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <EditOutlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal v-model:visible="visible" title="Edit tag" @ok="handleUpdate()">
    <a-form>
      <a-form-item label="Name">
        <a-input v-model:value="updatedTag.name" placeholder="Short tag name" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { reactive, ref } from "vue";
import { EditOutlined } from "@ant-design/icons-vue";
import useTags from "@/modules/tags";

export default {
  name: "TagUpdate",

  props: {
    tag: Object,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { updateTag } = useTags();
    const updatedTag = reactive({
      id: props.tag.id,
      name: props.tag.name,
    });
    async function handleUpdate() {
      await updateTag(updatedTag);
      visible.value = false;
    }

    return {
      updatedTag,
      handleUpdate,
      showModal,
      visible,
    };
  },

  components: { EditOutlined },
};
</script>