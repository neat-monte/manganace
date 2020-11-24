<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <edit-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Edit tag">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <edit-outlined />
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

    const { updateTagAsync } = useTags();
    const updatedTag = reactive({
      id: props.tag.id,
      name: props.tag.name,
    });
    async function handleUpdate() {
      await updateTagAsync(updatedTag);
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