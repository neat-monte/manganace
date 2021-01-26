<template>
  <a-button
    v-if="buttonText"
    type="primary"
    :disabled="disabled"
    @click="showModal()"
  >
    {{ buttonText }}
    <plus-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Create new research setting">
    <a-button type="primary" :disabled="disabled" @click="showModal()">
      <template v-slot:icon>
        <plus-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Create new research setting"
    @ok="handleCreate()"
  >
    <div class="create-research-setting">
      <div class="help">
        <p>
          The images are going to be picked from a pool of "good seeds" i.e.
          images that are by default in a neutral emotional state, centered, and
          looking straight.
        </p>
        <p>
          The pool of images is sorted, therefore, if
          <strong>overlap</strong> is set, then that amount of seeds will be
          picked in a sequential order guaranteeing the overlap in sessions with
          exact options.
        </p>
        <p>
          <strong>Slider ticks</strong> determine how many images each trial
          will require per slider. The default is <strong>21</strong> because it
          equally divides the range of [0,1] in 0.05 steps.
        </p>
        <p>
          <strong>Gender equalization</strong> attempts to make the count of
          male and female images equal. Nevertheless, if the total or
          overlapping amount is odd, then the preference will lie with female
          due to integer division.
        </p>
        <p>
          <strong>Global multiplier</strong> is a scalar for all the feature
          vectors.
        </p>
      </div>
      <a-form class="setting-data">
        <a-form-item label="Short name">
          <a-input v-model:value="newSetting.name" placeholder="Setting name" />
        </a-form-item>
        <a-form-item label="Image count in a session">
          <a-input-number
            v-model:value="newSetting.totalAmount"
            :min="1"
            :step="1"
          />
        </a-form-item>
        <a-form-item label="Overlapping images count">
          <a-input-number
            v-model:value="newSetting.overlapAmount"
            :min="0"
            :step="1"
          />
        </a-form-item>
      </a-form>
      <a-form class="setting-data">
        <a-form-item label="Global multiplier">
          <a-input-number
            v-model:value="newSetting.globalMultiplier"
            :min="0.001"
            :step="0.001"
          />
        </a-form-item>
        <a-form-item label="Slider ticks amount">
          <a-input-number
            v-model:value="newSetting.sliderSteps"
            :min="2"
            :step="1"
          />
        </a-form-item>
        <a-form-item label="Equalize gender">
          <a-switch v-model:checked="newSetting.equalizeGender" />
        </a-form-item>
      </a-form>
      <SessionExplanations :researchSetting="newSetting" />
    </div>
  </a-modal>
</template>

<script>
import { ref, reactive } from "vue";

import { PlusOutlined } from "@ant-design/icons-vue";
import SessionExplanations from "@/components/research/SessionExplanations";

import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "ResearchSettingCreate",

  props: {
    buttonText: {
      type: String,
      default: null,
    },
    disabled: Boolean,
  },

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }

    const { createResearchSettingAsync } = useResearchSettings();

    const newSetting = reactive({
      name: "",
      totalAmount: 1,
      overlapAmount: 0,
      sliderSteps: 21,
      equalizeGender: false,
      globalMultiplier: 0.1,
    });

    async function handleCreate() {
      visible.value = false;
      createResearchSettingAsync(newSetting);
    }

    return {
      newSetting,
      handleCreate,
      showModal,
      visible,
    };
  },

  components: {
    SessionExplanations,
    PlusOutlined,
  },
};
</script>

<style lang="scss" scoped>
.create-research-setting {
  display: flex;
  flex-wrap: wrap;
  text-align: justify;

  .setting-data {
    flex: 1;
    margin-right: 10px;
    margin-bottom: 20px;
  }
}
</style>