<template>
  <div class="session-select">
    <a-select
      v-model:value="value"
      show-search
      placeholder="Select a session"
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
import { ref } from "vue";
import useSessions from "@/modules/sessions";

export default {
  name: "SessionSelect",

  props: {
    showCreate: {
      type: Boolean,
      default: true,
    },
  },

  emits: ["session-id-set"],

  async setup(_, context) {
    const { loadSessionsAsync, sessionsById } = useSessions();

    const value = ref(undefined);

    function filterOption(input, option) {
      return option.props.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    }

    function handleChange(value) {
      context.emit("session-id-set", value);
    }

    await loadSessionsAsync();

    return {
      value,
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