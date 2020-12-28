<template>
  <a-button v-if="buttonText" type="danger" @click="showModal()">
    {{ buttonText }}
    <delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Delete research setting">
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <delete-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm research setting delete"
    @ok="handleDelete()"
  >
    <p>Remove the research setting</p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { DeleteOutlined } from "@ant-design/icons-vue";
import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "ResearchSettingDelete",

  props: {
    researchSettingId: Number,
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

    const { deleteResearchSettingAsync } = useResearchSettings();
    async function handleDelete() {
      visible.value = false;
      await deleteResearchSettingAsync(props.researchSettingId);
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