<template>
  <div class="research-setting-select">
    <a-select
      :value="currentResearchSetting.id"
      show-search
      :placeholder="placeholder"
      option-filter-prop="children"
      :filter-option="filterOption"
      @change="handleChange"
    >
      <a-select-option
        v-for="[id, setting] of Object.entries(researchSettingsById)"
        :key="setting.name"
        :value="Number(id)"
      >
        {{ setting.name }}
      </a-select-option>
    </a-select>
  </div>
</template>

<script>
import useResearchSettings from "@/modules/researchSettings";

export default {
  name: "ResearchSettingSelect",

  props: {
    placeholder: {
      type: String,
      default: "Select a research setting",
    },
  },

  emits: ["setting-id-set"],

  async setup(_, context) {
    const {
      loadResearchSettingsAsync,
      researchSettingsById,
      currentResearchSetting,
    } = useResearchSettings();

    function filterOption(input, option) {
      return option.props.key.toLowerCase().includes(input);
    }

    function handleChange(value) {
      context.emit("setting-id-set", value);
    }

    await loadResearchSettingsAsync();

    return {
      currentResearchSetting,
      researchSettingsById,
      filterOption,
      handleChange,
    };
  },
};
</script>

<style lang="scss" scoped>
.research-setting-select {
  display: flex;
  width: 100%;

  .ant-select {
    width: 100%;

    .ant-select-selection {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }
  }
}
</style>