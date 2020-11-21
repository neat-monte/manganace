<template>
  <div class="progress">
    <a-progress
      :percent="(currentSession.progress / currentSession.trials) * 100"
      :format="() => `${currentSession.progress} / ${currentSession.trials}`"
    />
  </div>

  <Trial v-if="!completed" :trial="trial" @complete="nextRandomTrial()" />

  <div v-else>
    <div class="title">Completed</div>
  </div>

  <div class="controls">
    <router-link :to="{ name: 'Research' }">
      <a-button type="default">
        <rollback-outlined />
        Exit
      </a-button>
    </router-link>
    <a-button type="primary" @click="next()">
      Next
      <caret-right-outlined />
    </a-button>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import { CaretRightOutlined, RollbackOutlined } from "@ant-design/icons-vue";
import Trial from "@/components/research/session/Trial";

import useResearch from "@/modules/research";

export default {
  name: "Trials",

  async setup() {
    const {
      currentSession,
      getTrialsMetaInfoAsync,
      saveChoiceAsync,
    } = useResearch();

    const progress = ref();
    const completed = ref(false);
    const trials = ref([]);
    const trial = ref();

    watchEffect(() => {
      progress.value = (currentSession.progress / currentSession.trials) * 100;
    });

    function nextRandomTrial() {
      if (trials.value.length === 0) {
        completed.value = true;
      } else {
        const randomIndex = Math.floor(Math.random() * trials.value.length);
        trial.value = trials.value[randomIndex];
        trials.value.splice(randomIndex, 1);
      }
    }

    async function next() {
      await saveChoiceAsync();
      nextRandomTrial();
    }

    trials.value = await getTrialsMetaInfoAsync();
    nextRandomTrial();

    return {
      currentSession,
      progress,
      completed,
      trial,
      trials,
      next,
    };
  },

  components: {
    Trial,
    CaretRightOutlined,
    RollbackOutlined,
  },
};
</script>

<style lang="scss" scoped>
.progress {
  // position: absolute;
  // right: -50px;
}

.controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>