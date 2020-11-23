<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Generate research session</span>
    </template>
    <a-button v-if="buttonText" type="primary" @click="showModal()">
      {{ buttonText }}
    </a-button>

    <a-button
      v-else-if="isAddon"
      type="primary"
      @click="showModal()"
      class="addon"
    >
      <template v-slot:icon>
        <plus-outlined />
      </template>
    </a-button>

    <a-button v-else type="primary" @click="showModal()">
      <template v-slot:icon>
        <plus-outlined />
      </template>
    </a-button>
  </a-tooltip>

  <a-modal
    v-model:visible="visible"
    title="Generate research session"
    @ok="handleCreate()"
  >
    <div class="create-session">
      <div class="help">
        <p>
          The images are going to be picked from a pool of "good seeds" i.e.
          images that are by default in a neutral emotional state, centered, and
          looking straight.
        </p>
        <p>
          The pool of images is sorted, therefore, if
          <strong>overlap</strong> is set, then that amount of seeds will be
          picked in a sequential order guaranteeing the overlap in sessions with
          exact options
        </p>
        <p>
          <strong>Slider ticks</strong> determine how many images each trial
          will require per slider. The default is <strong>21</strong> because it
          divides the range of [0,1].
        </p>
        <p>
          <strong>Gender equalization</strong> attempts to make the count of
          male and female images equal. Nevertheless, if the total or
          overlapping amount is odd, then the preference will lie with female
          due to integer division.
        </p>
      </div>
      <a-form class="session-data">
        <a-form-item label="Total image count">
          <a-input-number
            v-model:value="newSession.totalAmount"
            :min="1"
            :step="1"
          />
        </a-form-item>
        <a-form-item label="Overlapping images">
          <a-input-number
            v-model:value="newSession.overlapAmount"
            :min="0"
            :step="1"
          />
        </a-form-item>
      </a-form>
      <a-form class="session-data">
        <a-form-item label="Slider ticks amount">
          <a-input-number
            v-model:value="newSession.sliderSteps"
            :min="2"
            :step="1"
          />
        </a-form-item>
        <a-form-item label="Equalize gender">
          <a-switch v-model:checked="newSession.equalizeGender" />
        </a-form-item>
      </a-form>
      <div class="explanation">
        <p>There are <strong>6</strong> emotion vectors, therefore:</p>
        <ul>
          <li>
            <p>
              The new session will have
              <strong>{{ 6 * newSession.totalAmount }}</strong> trials.
            </p>
          </li>
          <li>
            <p>
              It will contain
              <strong>{{
                6 * newSession.totalAmount * newSession.sliderSteps
              }}</strong>
              images in total.
            </p>
          </li>
          <li>
            <p>
              The session <i>might</i> take around
              <strong>{{ duration }}</strong> to generate.
            </p>
          </li>
          <li>
            <p>
              It will require <i>approximately </i>
              <strong>{{ storage }}</strong> of space.
            </p>
          </li>
        </ul>
      </div>
    </div>
  </a-modal>
</template>

<script>
import { ref, reactive, watchEffect } from "vue";
import moment from "moment";

import { PlusOutlined } from "@ant-design/icons-vue";
import useResearch from "@/modules/research";

export default {
  name: "SessionCreate",

  props: {
    buttonText: {
      type: String,
      default: null,
    },
    isAddon: {
      type: Boolean,
      default: false,
    },
  },

  setup() {
    const visible = ref();
    function showModal() {
      visible.value = true;
    }
    const duration = ref();
    const storage = ref();

    const { addSessionAsync } = useResearch();

    const newSession = reactive({
      totalAmount: 1,
      overlapAmount: 0,
      sliderSteps: 21,
      equalizeGender: false,
    });

    watchEffect(() => {
      const seconds = 1.5 * 6 * newSession.totalAmount * newSession.sliderSteps;
      const dur = moment.duration(seconds, "seconds");
      const hours = Math.floor(dur.asHours());
      const minutes = Math.floor(dur.asMinutes()) - hours * 60;
      if (hours <= 0) {
        duration.value = `${minutes} minutes`;
      } else {
        duration.value = `${hours} hours ${minutes} minutes`;
      }
      const bytes =
        1413040 * 6 * newSession.totalAmount * newSession.sliderSteps;
      const megabytes = Math.floor(bytes / 1048576);
      const gigabytes = (megabytes / 1024).toFixed(2);
      if (gigabytes < 1) {
        storage.value = `${megabytes} MB`;
      } else {
        storage.value = `${gigabytes} GB`;
      }
    });

    async function handleCreate() {
      await addSessionAsync(newSession);
      visible.value = false;
    }

    return {
      newSession,
      handleCreate,
      showModal,
      visible,
      duration,
      storage,
    };
  },

  components: {
    PlusOutlined,
  },
};
</script>

<style lang="scss" scoped>
.addon {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.create-session {
  display: flex;
  flex-wrap: wrap;
  text-align: justify;

  .help {
    flex: 1 100%;
  }

  .session-data {
    flex: 50%;
    margin-bottom: 20px;
  }

  .explanation {
    flex: 1 100%;
  }
}
</style>