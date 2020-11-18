<template>
  <div id="sessions">
    <div class="controls">
      <CreateSession buttonText="Initialize new session" />
    </div>

    <a-list
      :grid="{ gutter: 50, xs: 1, md: 2, lg: 2, xl: 3, xxl: 4 }"
      :data-source="sessions"
    >
      <template #renderItem="{ item, index }">
        <a-list-item :key="index" class="session-content">
          <div class="options">
            <a-descriptions size="small" :column="2">
              <a-descriptions-item label="Images count">
                <span>{{ item.totalAmount }}</span>
              </a-descriptions-item>
              <a-descriptions-item label="Overlapping">
                <span>{{ item.overlapAmount }}</span>
              </a-descriptions-item>
              <a-descriptions-item label="Gender eq.">
                <span>{{ item.equalizeGender ? "Yes" : "No" }}</span>
              </a-descriptions-item>
              <a-descriptions-item label="Slider steps">
                <span>{{ item.sliderSteps }}</span>
              </a-descriptions-item>
              <a-descriptions-item label="Trials count">
                <span>{{ item.trials }}</span>
              </a-descriptions-item>
              <a-descriptions-item label="Done trials">
                <span>{{ item.progress }}</span>
              </a-descriptions-item>
            </a-descriptions>
          </div>

          <div class="progress">
            <a-progress
              :percent="item.progress > 0 ? item.trials / item.progress : 0"
            />
            <div class="actions">
              <a-button type="primary" :disabled="item.trials == item.progress">
                {{ item.progress == 0 ? "Begin" : "Continue" }}
              </a-button>
            </div>
          </div>
        </a-list-item>
      </template>
    </a-list>
  </div>
</template>

<script>
import { watchEffect, ref } from "vue";

import CreateSession from "@/components/actions/research/CreateSession";

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
  },
};
</script>

<style lang="scss" scoped>
#sessions {
  height: 100%;
  margin: 0 10px;

  .controls {
    text-align: right;
    margin-bottom: 20px;
  }

  .session-content {
    padding: 0 20px;

    .progress {
      align-items: center;
      display: flex;

      .actions {
        width: 35%;
        margin-left: 20px;
        text-align: right;
      }
    }
  }
}

@include tablet {
  #sessions {
    margin: 0;
  }
}
</style>