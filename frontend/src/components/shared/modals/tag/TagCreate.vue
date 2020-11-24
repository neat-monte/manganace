<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <plus-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Create new tag">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <plus-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Create new tag"
    @ok="handleCreate()"
  >
    <a-form>
      <a-form-item label="Name">
        <a-input v-model:value="newTag.name" placeholder="Short tag name" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { ref, reactive } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";
import useTags from "@/modules/tags";

export default {
  name: "TagCreate",

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

    const { createTagAsync } = useTags();
    const newTag = reactive({
      name: null,
    });
    async function handleCreate() {
      await createTagAsync(newTag);
      visible.value = false;
    }

    return {
      newTag,
      handleCreate,
      showModal,
      visible,
    };
  },

  components: {
    PlusOutlined,
  },
};
</script>