<template>
  <div id="participation">
    <Introduction v-if="step === 1" />
    <Consent
      v-else-if="step === 2"
      v-model:consent="participant.consented"
      @change="participant.consentedOn = moment().toISOString()"
    />
    <Suspense v-else>
      <template #default>
        <Demographics
          v-model:age="participant.age"
          v-model:genderId="participant.genderId"
        />
      </template>
      <template #fallback>
        <Loading />
      </template>
    </Suspense>
    <div class="controls">
      <router-link :to="{ name: 'Research' }">
        <a-button type="default">
          <rollback-outlined />
          Exit
        </a-button>
      </router-link>
      <div class="navigation">
        <a-button v-if="step > 1" type="primary" @click="prev">
          <caret-left-outlined />
          Back
        </a-button>

        <a-button
          type="primary"
          @click="next"
          :disabled="
            (step === 2 && !participant.consented) || (step === 3 && !isValid())
          "
        >
          {{ step === 3 ? "Begin" : "Next" }}
          <caret-right-outlined />
        </a-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import moment from "moment";

import {
  CaretRightOutlined,
  CaretLeftOutlined,
  RollbackOutlined,
} from "@ant-design/icons-vue";

import Introduction from "@/components/research/session/participation/Introduction";
import Consent from "@/components/research/session/participation/Consent";
import Demographics from "@/components/research/session/participation/Demographics";
import Loading from "@/components/shared/display/Loading";

import useResearchParticipant from "@/modules/researchParticipant";

export default {
  name: "Participation",

  props: {
    session: {
      type: Object,
      required: true,
    },
  },

  setup(props) {
    const { assignParticipantAsync } = useResearchParticipant();

    const participant = reactive({
      age: null,
      genderId: null,
      consented: false,
      consentedOn: null,
      sessionId: props.session.id,
    });

    const isValid = () =>
      participant.consented &&
      participant.age &&
      18 <= participant.age &&
      participant.genderId;

    const step = ref(1);

    async function next() {
      switch (step.value) {
        case 1:
          step.value++;
          break;
        case 2:
          if (participant.consented) {
            step.value++;
          }
          break;
        case 3:
          if (isValid()) {
            await assignParticipantAsync(
              props.session.researchSettingId,
              participant
            );
          }
          break;
      }
    }

    function prev() {
      step.value--;
    }

    return {
      participant,
      isValid,
      step,
      next,
      prev,
      moment,
    };
  },

  components: {
    Introduction,
    Consent,
    Demographics,
    Loading,
    CaretRightOutlined,
    CaretLeftOutlined,
    RollbackOutlined,
  },
};
</script>

<style lang="scss" scoped>
#participation {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .controls {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;

    .navigation {
      > *:last-child {
        margin-left: 20px;
      }
    }
  }
}
</style>