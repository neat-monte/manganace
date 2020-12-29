<template>
  <a-button v-if="buttonText" type="danger" @click="showModal()">
    {{ buttonText }}
    <delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Delete generator session">
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm generator session delete"
    @ok="handleDelete()"
  >
    <p>
      The generator session and all the generated images will be removed.
      <strong>It will be unrecoverable.</strong>
    </p>
    <p>
      <i>
        This action will only succeed if no images are saved to any collection.
      </i>
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import useGeneratorSessions from "@/modules/generatorSessions";

export default {
  name: "GeneratorSessionDelete",

  props: {
    generatorSessionId: Number,
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

    const { deleteGeneratorSessionAsync } = useGeneratorSessions();

    async function handleDelete() {
      visible.value = false;
      await deleteGeneratorSessionAsync(props.generatorSessionId);
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