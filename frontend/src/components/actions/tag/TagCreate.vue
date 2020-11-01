<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Create new tag</span>
    </template>
    <a-button v-if="isAddon" type="primary" @click="showModal()" class="addon">
      <template v-slot:icon>
        <PlusOutlined />
      </template>
    </a-button>

    <a-button v-else type="primary" shape="circle" @click="showModal()">
      <template v-slot:icon>
        <PlusOutlined />
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
import notification from "@/services/notification";
import useTags from "@/modules/useTags";

export default {
  name: "TagCreate",

  props: {
    isAddon: {
      type: Boolean,
      default: false,
    },
  },

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { addTag } = useTags();
    const newTag = reactive({
      name: null,
    });
    async function handleCreate() {
      const created = await addTag(newTag);
      visible.value = false;
      notification.tags.created(created);
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

<style lang="scss" scoped>
.addon {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  box-shadow: none !important;
}
</style>