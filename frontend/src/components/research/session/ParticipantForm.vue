<template>
  <div id="participant-form">
    <div class="title">INTRODUCTION</div>
    <p>
      You are invited to participate in a research project which is being
      conducted by a bachelor's student at Radboud University. The procedure
      involves moving a slider and looking at human face images, which will take
      <i>approximately</i> <strong>30 minutes</strong>. Your participation in
      this research study is voluntary and you may withdraw at any time.
      <strong>The data collected will be made fully anonymous.</strong>
    </p>
    <div class="title">INSTRUCTIONS</div>
    <p>
      The pursose of this study is to investigate the natural perception of
      emotion. You will be provided with a single emotion, a slider and an image
      of a person. By moving the slider to the right, the mentioned emotion will
      be applied stronger on the displayed face. On the other hand, by moving
      the slider to the left, the emotion will be reduced. The task is to place
      the slider where you think the provided emotion looks most natural on the
      person's face.
    </p>
    <p>
      Should you want more information on the research project, please feel free
      to contact the student at
      <strong>m.makelis@student.ru.nl</strong>
    </p>
    <a-form class="form">
      <a-form-item label="Age">
        <a-input-number v-model:value="participant.age" />
      </a-form-item>
      <a-form-item label="Gender">
        <a-radio-group v-model:value="participant.genderId">
          <a-radio
            v-for="gender in genderOptions"
            :key="gender.id"
            :value="gender.id"
            class="radio"
          >
            {{ gender.option }}
          </a-radio>
        </a-radio-group>
      </a-form-item>
    </a-form>
    <div class="controls">
      <router-link :to="{ name: 'Research' }">
        <a-button type="default">
          <rollback-outlined />
          Exit
        </a-button>
      </router-link>
      <a-button type="primary" :disabled="!isValid()" @click="beginSession()">
        Begin
        <caret-right-outlined />
      </a-button>
    </div>
  </div>
</template>

<script>
import { reactive, ref, watchEffect } from "vue";

import { CaretRightOutlined, RollbackOutlined } from "@ant-design/icons-vue";

import useResearch from "@/modules/research";
import useExtras from "@/modules/extras";

export default {
  name: "ParticipantForm",

  async setup() {
    const { currentSession, assignParticipantAsync } = useResearch();
    const {
      loadGendersAsync,
      gendersById,
    } = useExtras();

    const genderOptions = ref([]);

    watchEffect(() => {
      genderOptions.value = Object.values(gendersById);
    });

    const participant = reactive({
      age: null,
      genderId: null,
      sessionId: currentSession.id,
    });

    const isValid = () =>
      participant.age &&
      18 <= participant.age &&
      participant.genderId;

    async function beginSession() {
      await assignParticipantAsync(participant);
    }

    await loadGendersAsync();

    return {
      participant,
      genderOptions,
      isValid,
      beginSession,
    };
  },

  components: {
    CaretRightOutlined,
    RollbackOutlined,
  },
};
</script>

<style lang="scss" scoped>
#participant-form {
  p {
    text-align: justify;
  }

  .form {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-bottom: 40px;

    .radio {
      display: block;
      height: 30px;
      line-height: 30px;
    }
  }

  .controls {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
}
</style>