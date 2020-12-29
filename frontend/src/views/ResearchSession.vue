<template>
  <div id="research-session" class="content">
    <div class="session-wrapper">
      <Participation
        v-if="!currentSession.participant"
        :session="currentSession"
      />
      <Suspense v-else>
        <template #default>
          <Trials :session="currentSession" />
        </template>
        <template #fallback>
          <Loading />
        </template>
      </Suspense>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

import Participation from "@/components/research/session/Participation";
import Trials from "@/components/research/session/Trials";
import Loading from "@/components/shared/display/Loading";

import useResearchSessions from "@/modules/researchSessions";

export default {
  name: "ResearchSession",

  setup() {
    const router = useRouter();
    const { currentSession } = useResearchSessions();

    if (!currentSession.id) {
      router.push({
        name: "Research",
      });
    }

    return {
      currentSession,
    };
  },

  components: {
    Participation,
    Trials,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#research-session {
  padding-top: $header-height;
  display: flex;
  height: 100%;
  align-content: center;
  justify-content: center;

  .session-wrapper {
    position: relative;
    flex: 100%;
    padding: 20px;
  }
}

@include tablet {
  #research-session {
    .session-wrapper {
      padding: 0 15%;
    }
  }
}
</style>