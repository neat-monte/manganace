<template>
  <a-button
    v-if="buttonText"
    type="danger"
    :disabled="disabled"
    @click="showModal()"
  >
    {{ buttonText }}
    <delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" :title="tooltip">
    <a-button type="danger" :disabled="disabled" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
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
    buttonText: {
      type: String,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    tooltip: {
      type: String,
      default: "Delete tag",
    },
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { deleteTagAsync } = useTags();
    async function handleDelete() {
      visible.value = false;
      await deleteTagAsync(props.tagId);
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