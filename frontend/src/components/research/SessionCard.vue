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
        v-if="session.participant"
        size="small"
        :column="2"
        layout="horizontal"
        :bordered="true"
      >
        <a-descriptions-item label="Age">
          <span>{{ session.participant.age }}</span>
        </a-descriptions-item>
        <a-descriptions-item label="Gender">
          <span>{{ gendersById[session.participant.genderId].name }}</span>
        </a-descriptions-item>
      </a-descriptions>
      <p v-else>No participant yet</p>
    </div>
    <div class="card-controls">
      <ParticipantDelete
        v-if="session.participant"
        :researchSettingId="session.researchSettingId"
        :participantId="session.participant.id"
      />
      <ResearchSessionDelete v-else :researchSessionId="session.id" />
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
import ParticipantDelete from "@/components/shared/modals/participant/ParticipantDelete";
import ResearchSessionDelete from "@/components/shared/modals/session/ResearchSessionDelete";

import useResearchSessions from "@/modules/researchSessions";
import useExtras from "@/modules/extras";

export default {
  name: "SessionCard",

  props: {
    session: Object,
  },

  setup(props) {
    const router = useRouter();
    const { gendersById } = useExtras();
    const { setCurrentSession } = useResearchSessions();

    function startSession() {
      setCurrentSession(props.session.researchSettingId, props.session.id);
      router.push({
        name: "ResearchSession",
      });
    }

    return {
      gendersById,
      startSession,
    };
  },

  components: {
    SessionResults,
    ParticipantDelete,
    ResearchSessionDelete,
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

  .information {
    min-height: 40px;

    > p {
      margin: 0;
    }
  }

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

    .additional-controls {
      position: absolute;
      left: 10px;
      color: $primary;
    }
  }

  &:hover {
    .card-controls {
      bottom: 0;
      visibility: visible;
    }
  }
}
</style>