<template>
  <div id="research-session" class="content">
    <div class="session-wrapper">
      <Suspense v-if="!currentSession.participant">
        <template #default>
          <ParticipantForm />
        </template>
        <template #fallback>
          <Loading />
        </template>
      </Suspense>
      <Suspense v-else>
        <template #default>
          <Trials />
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

import ParticipantForm from "@/components/research/session/ParticipantForm";
import Trials from "@/components/research/session/Trials";
import Loading from "@/components/shared/Loading";

import useResearch from "@/modules/research";

export default {
  name: "ResearchSession",

  setup() {
    const router = useRouter();
    const { currentSession } = useResearch();

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
    ParticipantForm,
    Trials,
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#research-session {
  padding-top: $header-height / 2;
  display: flex;
  height: 100%;
  align-content: center;
  justify-content: center;

  .session-wrapper {
    position: relative;
    flex: 100%;
  }
}
</style>