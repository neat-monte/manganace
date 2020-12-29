<template>
  <a-button v-if="buttonText" type="danger" @click="showModal()">
    {{ buttonText }}
    <user-delete-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Delete participant">
    <a-button type="danger" @click="showModal()">
      <template v-slot:icon>
        <user-delete-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Confirm participant delete"
    @ok="handleDelete()"
  >
    <p>
      The participant and all the data will be removed.
      <strong>It will be unrecoverable.</strong>
    </p>
  </a-modal>
</template>

<script>
import { ref } from "vue";
import { UserDeleteOutlined } from "@ant-design/icons-vue";
import useResearchParticipant from "@/modules/researchParticipant";

export default {
  name: "ParticipantDelete",

  props: {
    researchSettingId: Number,
    participantId: Number,
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

    const { deleteParticipantAsync } = useResearchParticipant();

    async function handleDelete() {
      visible.value = false;
      await deleteParticipantAsync(
        props.researchSettingId,
        props.participantId
      );
    }

    return {
      handleDelete,
      showModal,
      visible,
    };
  },

  components: { UserDeleteOutlined },
};
</script>