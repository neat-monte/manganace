<template>
  <a-button
    v-if="buttonText"
    type="primary"
    :disabled="disabled"
    @click="showModal()"
  >
    {{ buttonText }}
    <sync-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Generate research session">
    <a-button type="primary" :disabled="disabled" @click="showModal()">
      <template v-slot:icon>
        <sync-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Generate research session"
    @ok="handleCreate()"
  >
    <div class="create-session">
      <div class="help">
        <p>Choose the <strong>amount</strong> to generate.</p>
        <p>
          Set the <strong>batch size</strong> to the appropriate number for your
          GPU memory. It seems that for 8GB of DRAM batch size of 8 was maximum,
          although up to 10 also worked but with memory shortage warnings. If
          the batch number is too high - you will encounter a memory shortage
          error which will not allow to initialize the generator.
        </p>
      </div>
      <a-form class="session-data">
        <a-form-item label="Amount to generate">
          <a-input-number v-model:value="amount" :min="1" :step="1" />
        </a-form-item>
      </a-form>
      <a-form class="session-data">
        <a-form-item label="Batch size to use">
          <a-input-number
            v-model:value="newSession.batchSize"
            :min="1"
            :step="1"
          />
        </a-form-item>
      </a-form>
      <SessionExplanations
        :researchSetting="researchSettingsById[researchSettingId]"
        :amount="amount"
      />
    </div>
  </a-modal>
</template>

<script>
import { ref, reactive } from "vue";

import { SyncOutlined } from "@ant-design/icons-vue";
import SessionExplanations from "@/components/research/SessionExplanations";

import useResearchSessions from "@/modules/researchSessions";
import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "ResearchSessionCreate",

  props: {
    researchSettingId: {
      type: Number,
      required: true,
    },
    buttonText: {
      type: String,
      default: null,
    },
    disabled: Boolean,
  },

  setup(props) {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { createResearchSessionsAsync } = useResearchSessions();
    const { researchSettingsById } = useResearchSettings();

    const amount = ref(1);

    const newSession = reactive({
      batchSize: 8,
      session: {
        researchSettingId: props.researchSettingId,
      },
    });

    async function handleCreate() {
      visible.value = false;
      await createResearchSessionsAsync(newSession, amount.value);
    }

    return {
      researchSettingsById,
      amount,
      newSession,
      handleCreate,
      showModal,
      visible,
    };
  },

  components: {
    SessionExplanations,
    SyncOutlined,
  },
};
</script>

<style lang="scss" scoped>
.create-session {
  display: flex;
  flex-wrap: wrap;
  text-align: justify;

  .session-data {
    flex: 50%;
    margin-bottom: 20px;
  }
}
</style>