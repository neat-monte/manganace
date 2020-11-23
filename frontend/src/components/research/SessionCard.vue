<template>
  <div class="session-card">
    <div class="progress">
      <a-progress
        :percent="Math.floor((session.progress / session.trials) * 100)"
        :format="() => `${session.progress} / ${session.trials}`"
      />
    </div>
    <div class="information">
      <a-descriptions
        size="small"
        :column="2"
        layout="horizontal"
        :bordered="true"
      >
        <a-descriptions-item label="Image #">
          <span>{{ session.totalAmount }}</span>
        </a-descriptions-item>
        <a-descriptions-item label="Overlapping">
          <span>{{ session.overlapAmount }}</span>
        </a-descriptions-item>
        <a-descriptions-item label="Gender eq.">
          <span>{{ session.equalizeGender ? "Yes" : "No" }}</span>
        </a-descriptions-item>
        <a-descriptions-item label="Sl. steps">
          <span>{{ session.sliderSteps }}</span>
        </a-descriptions-item>
        <a-descriptions-item label="Has participant">
          <span>{{ session.participant ? "Yes" : "No" }}</span>
        </a-descriptions-item>
      </a-descriptions>
    </div>
    <div class="card-controls">
      <Suspense>
        <template #default>
          <SessionResults :session="session" />
        </template>
      </Suspense>
      <a-button
        v-if="session.trials !== session.progress"
        type="primary"
        @click="startSession()"
      >
        {{ !session.participant ? "Begin" : "Continue" }}
        <caret-right-outlined />
      </a-button>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import { CaretRightOutlined } from "@ant-design/icons-vue";
import SessionResults from "@/components/research/SessionResults";

import useResearch from "@/modules/research";

export default {
  name: "SessionCard",

  props: {
    session: Object,
  },

  setup(props) {
    const router = useRouter();
    const { setCurrentSession } = useResearch();

    function startSession() {
      setCurrentSession(props.session.id);
      router.push({
        name: "ResearchSession",
      });
    }

    return {
      startSession,
    };
  },

  components: {
    SessionResults,
    CaretRightOutlined,
  },
};
</script>

<style lang="scss" scoped>
.session-card {
  position: relative;
  overflow: hidden;
  border: 1px solid $darkness-20;
  background: $darkness-05;
  border-radius: 2px;
  padding: 10px 10px;

  .progress {
    padding: 0 30px 10px 10px;
  }

  .card-controls {
    position: absolute;
    background: $filler-80;
    left: 0;
    bottom: -100%;
    transition: all 0.2s ease;
    visibility: hidden;
    padding: 10px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    width: 100%;
  }

  &:hover {
    .card-controls {
      bottom: 0;
      visibility: visible;
    }
  }
}
</style>