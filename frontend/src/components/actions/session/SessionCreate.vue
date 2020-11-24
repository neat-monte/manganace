<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
  </a-button>

  <a-button
    v-else-if="isAddon"
    type="primary"
    @click="showModal()"
    class="addon"
  >
    <template v-slot:icon>
      <plus-outlined />
    </template>
  </a-button>

  <a-tooltip v-else placement="top" title="Create new session">
    <a-button type="primary" @click="showModal()">
      <template v-slot:icon>
        <plus-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Create new session"
    @ok="handleCreate()"
  >
    <a-form>
      <a-form-item label="Name">
        <a-input v-model:value="newSession.name" placeholder="Session name" />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import { ref, reactive } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";
import useSessions from "@/modules/sessions";

export default {
  name: "SessionCreate",

  props: {
    buttonText: {
      type: String,
      default: null,
    },
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

    const { addSessionAsync } = useSessions();
    const newSession = reactive({
      name: null,
    });
    async function handleCreate() {
      await addSessionAsync(newSession);
      visible.value = false;
    }

    return {
      newSession,
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
}
</style>