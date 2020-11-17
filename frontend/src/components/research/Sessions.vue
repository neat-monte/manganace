<template>
  <div id="sessions">
    <a-list item-layout="horizontal" :data-source="sessions">
      <template #renderItem="{ item, index }">
        <a-list-item :key="index">
          <a-list-item-meta>
            {{ index }}
            <template #title> Total: {{ item.totalAmount }} </template>
          </a-list-item-meta>
        </a-list-item>
      </template>
    </a-list>
  </div>
</template>

<script>
import { watchEffect, ref } from "vue";
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
};
</script>