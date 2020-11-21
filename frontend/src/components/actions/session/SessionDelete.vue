<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Delete session</span>
    </template>
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm session delete"
    @ok="handleDelete()"
  >
    <p>
      The session will be removed with all the generated images.
      <strong>It will be unrecoverable.</strong>
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import useSessions from "@/modules/sessions";

export default {
  name: "SessionDelete",

  props: {
    sessionId: Number,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteSessionAsync } = useSessions();
    async function handleDelete() {
      await deleteSessionAsync(props.sessionId);
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