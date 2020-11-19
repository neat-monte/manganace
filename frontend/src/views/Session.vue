<template>
  <div id="session" class="content">
    <Suspense v-if="!(session && session.participant)">
      <template #default>
        <ParticipantForm />
      </template>
      <template #fallback>
        <Loading />
      </template>
    </Suspense>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import ParticipantForm from "@/components/session/ParticipantForm";
import Loading from "@/components/shared/Loading";

import useResearch from "@/modules/research";

export default {
  name: "Session",

  setup() {
    const { sessionsById, currentSessionId, loadSessionsAsync } = useResearch();
    const session = ref(null);

    loadSessionsAsync();

    watchEffect(() => {
      session.value = sessionsById[currentSessionId];
    });

    return {
      session,
      sessionsById,
    };
  },

  components: {
    ParticipantForm,
    Loading,
  },
};
</script>