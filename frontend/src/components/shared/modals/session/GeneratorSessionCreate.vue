<template>
  <a-button v-if="buttonText" type="primary" @click="showModal()">
    {{ buttonText }}
    <plus-outlined />
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
  name: "GeneratorSessionCreate",

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

    const { createGeneratorSessionAsync } = useSessions();
    const newSession = reactive({
      name: null,
    });
    async function handleCreate() {
      visible.value = false;
      await createGeneratorSessionAsync(newSession);
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