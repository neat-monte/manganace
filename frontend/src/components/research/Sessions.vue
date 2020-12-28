<template>
  <Loading v-if="loading" id="sessions" />
  <div v-else id="sessions">
    <div class="controls">
      <div v-if="researchGenerateRequest.inProgress" class="current-job">
        <Loading />
        Generating
        {{
          researchGenerateRequest.total > 1
            ? `${researchGenerateRequest.done} / ${researchGenerateRequest.total} sessions`
            : "a session"
        }}
      </div>
      <div class="buttons">
        <ResearchSessionCreate
          :researchSettingId="researchSettingId"
          buttonText="Generate session"
          :disabled="researchGenerateRequest.inProgress"
        />
      </div>
    </div>

    <a-list
      :grid="{ gutter: 20, xs: 1, md: 2, lg: 2, xl: 3, xxl: 4 }"
      :data-source="sessionsBySettingId[researchSettingId]"
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

import ResearchSessionCreate from "@/components/shared/modals/session/ResearchSessionCreate";
import SessionCard from "@/components/research/SessionCard";
import Loading from "@/components/shared/display/Loading";

import useResearchSessions from "@/modules/researchSessions";
import useExtras from "@/modules/extras";

export default {
  name: "Sessions",

  props: {
    researchSettingId: {
      type: Number,
      required: true,
    },
  },

  async setup(props) {
    const loading = ref();
    const {
      sessionsBySettingId,
      loadResearchSessionsAsync,
      researchGenerateRequest,
    } = useResearchSessions();
    const { loadGendersAsync } = useExtras();

    watchEffect(async () => {
      loading.value = true;
      await loadResearchSessionsAsync(props.researchSettingId);
      loading.value = false;
    });

    await loadGendersAsync();

    return {
      loading,
      researchGenerateRequest,
      sessionsBySettingId,
    };
  },

  components: {
    ResearchSessionCreate,
    SessionCard,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#sessions {
  height: 100%;
  margin: 0 10px;

  .controls {
    display: flex;
    justify-content: space-between;

    margin-bottom: 20px;

    .current-job {
      flex: 0 220px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .buttons {
      flex: 1;
      text-align: right;
    }
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