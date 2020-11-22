<template>
  <div id="sessions">
    <div class="controls">
      <CreateSession buttonText="Initialize new session" />
    </div>

    <a-list
      :grid="{ gutter: 20, xs: 1, md: 2, lg: 2, xl: 3, xxl: 4 }"
      :data-source="sessions"
    >
      <template #renderItem="{ item, index }">
        <a-list-item :key="index">
          <SessionCard :session="item" />
        </a-list-item>
      </template>
    </a-list>
  </div>
</template>

<script>
import { watchEffect, ref } from "vue";

import CreateSession from "@/components/actions/research/CreateSession";
import SessionCard from "@/components/research/SessionCard";

import useResearch from "@/modules/research";

export default {
  name: "Sessions",

  async setup() {
    const { sessionsById, loadSessionsAsync } = useResearch();

    const sessions = ref([]);

    watchEffect(() => {
      sessions.value = Object.values(sessionsById);
    });

    await loadSessionsAsync();

    return {
      sessions,
    };
  },

  components: {
    CreateSession,
    SessionCard,
  },
};
</script>

<style lang="scss" scoped>
#sessions {
  height: 100%;
  margin: 0 10px;

  .controls {
    text-align: right;
    margin: 0 18% 20px 0;
  }
}

@include tablet {
  #sessions {
    margin: 0;

    .controls {
      margin-right: 0;
    }
  }
}
</style>