<template>
  <div id="sessions">
    <div v-if="!currentSession.id" class="no-session-selected">
      <span class="message">Choose</span>
      <Suspense>
        <template #default>
          <GeneratorSessionSelect
            placeholder="an already existing"
            @session-id-set="setSession"
          />
        </template>
        <template #fallback>
          <span class="message">an already existing</span>
        </template>
      </Suspense>
      <span class="message">session or</span>
      <GeneratorSessionCreate buttonText="Create" />
      <span class="message">new session</span>
    </div>

    <div v-else class="session-selected">
      <div class="controls">
        <span class="title">{{ currentSession.name }}</span>
        <div class="floating">
          <div>
            <GeneratorSessionDelete :generatorSessionId="currentSession.id" />
          </div>
          <div>
            <a-button
              type="primary"
              @click="nullifySession"
              class="change-session"
            >
              Change session
              <swap-outlined />
            </a-button>
          </div>
        </div>
      </div>
      <Suspense>
        <template #default>
          <Activity :sessionId="currentSession.id" />
        </template>
        <template #fallback>
          <Loading id="activity" />
        </template>
      </Suspense>
    </div>
  </div>
</template>

<script>
import { SwapOutlined } from "@ant-design/icons-vue";
import Activity from "@/components/generator/Activity";
import GeneratorSessionSelect from "@/components/shared/controls/GeneratorSessionSelect";
import GeneratorSessionCreate from "@/components/shared/modals/session/GeneratorSessionCreate";
import GeneratorSessionDelete from "@/components/shared/modals/session/GeneratorSessionDelete";
import Loading from "@/components/shared/display/Loading";

import useGeneratorSessions from "@/modules/generatorSessions";
import useGenerator from "@/modules/generator";

export default {
  name: "Sessions",

  async setup() {
    const {
      sessionsById,
      currentSession,
      setCurrentSession,
    } = useGeneratorSessions();
    const { nullifyImage } = useGenerator();

    function setSession(sessionId) {
      setCurrentSession(sessionsById[sessionId]);
    }

    function nullifySession() {
      setCurrentSession(null);
      nullifyImage();
    }

    return {
      currentSession,
      setSession,
      nullifySession,
    };
  },

  components: {
    Loading,
    GeneratorSessionSelect,
    GeneratorSessionCreate,
    GeneratorSessionDelete,
    Activity,
    SwapOutlined,
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

    .controls {
      position: relative;
      margin-bottom: 5px;

      & > * {
        flex: 1;
      }

      .floating {
        display: flex;
        justify-content: flex-end;

        & > *:not(:last-child) {
          margin-right: 5px;
        }
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

@include sm-desktop {
  #sessions {
    .session-selected {
      .controls {
        .floating {
          position: absolute;
          top: 2px;
          right: 0;
        }
      }
    }
  }
}
</style>