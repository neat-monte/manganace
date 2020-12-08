<template>
  <div class="session-select">
    <a-select
      :value="currentSession.id"
      show-search
      :placeholder="placeholder"
      option-filter-prop="children"
      :filter-option="filterOption"
      @change="handleChange"
    >
      <a-select-option
        v-for="[id, session] of Object.entries(sessionsById)"
        :key="session.name"
        :value="Number(id)"
      >
        {{ session.name }}
      </a-select-option>
    </a-select>
  </div>
</template>

<script>
import useSessions from "@/modules/sessions";
import useGenerator from "@/modules/generator";

export default {
  name: "GeneratorSessionSelect",

  props: {
    placeholder: {
      type: String,
      default: "Select a session",
    },
  },

  emits: ["session-id-set"],

  async setup(_, context) {
    const { loadGeneratorSessionsAsync, sessionsById } = useSessions();
    const { currentSession } = useGenerator();

    function filterOption(input, option) {
      return option.props.key.toLowerCase().includes(input);
    }

    function handleChange(value) {
      context.emit("session-id-set", value);
    }

    await loadGeneratorSessionsAsync();

    return {
      currentSession,
      sessionsById,
      filterOption,
      handleChange,
    };
  },
};
</script>

<style lang="scss" scoped>
.session-select {
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