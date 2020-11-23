<template>
  <div id="sessions">
    <div v-if="!currentSession.id" class="no-session-selected">
      <span class="message">Choose</span>
      <Suspense>
        <template #default>
          <SessionSelect
            placeholder="an already existing"
            @session-id-set="setSession"
          />
        </template>
        <template #fallback>
          <span class="message">an already existing</span>
        </template>
      </Suspense>
      <span class="message">session or</span>
      <SessionCreate buttonText="Create" />
      <span class="message">new session</span>
    </div>

    <div v-else class="session-selected">
      <div class="header">
        <span class="title">{{ currentSession.name }}</span>
        <a-button type="primary" @click="nullifySession" class="change-session">
          Change session
        </a-button>
      </div>
      <Suspense>
        <template #default>
          <Activity />
        </template>
        <template #fallback>
          <Loading id="activity" />
        </template>
      </Suspense>
    </div>
  </div>
</template>

<script>
import Activity from "@/components/generator/Activity";
import SessionSelect from "@/components/actions/session/SessionSelect";
import SessionCreate from "@/components/actions/session/SessionCreate";
import Loading from "@/components/shared/Loading";
import useGenerator from "@/modules/generator";
import useSessions from "@/modules/sessions";

export default {
  name: "Sessions",

  async setup() {
    const { sessionsById } = useSessions();
    const { setCurrentSession, currentSession } = useGenerator();

    function setSession(sessionId) {
      setCurrentSession(sessionsById[sessionId]);
    }

    function nullifySession() {
      setCurrentSession(null);
    }

    return {
      currentSession,
      setSession,
      nullifySession,
    };
  },

  components: {
    Loading,
    SessionSelect,
    SessionCreate,
    Activity,
  },
};
</script>

<style lang="scss" scoped>
#sessions {
  max-width: 100%;
  padding: 20px 0;
  display: flex;
  flex-direction: column;

  .no-session-selected {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;

    .message {
      font-size: 1.4rem;
      font-weight: bold;
      color: $primary;
      margin: 0 10px;
    }

    .session-select {
      width: 200px;
    }
  }

  .session-selected {
    padding: 0 20px;

    .header {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;
      position: relative;
      padding-right: 150px;

      .change-session {
        position: absolute;
        right: 0;
      }
    }
  }
}

@include tablet {
  #sessions {
    .session-selected {
      padding: 0;
    }
  }
}
</style>