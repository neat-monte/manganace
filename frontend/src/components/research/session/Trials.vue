<template>
  <div id="trials">
    <div class="progress">
      <a-progress
        :percent="(session.progress / session.trials) * 100"
        :format="() => `${session.progress} / ${session.trials}`"
      />
    </div>
    <div v-if="!completed" class="trial">
      <div class="trial-description">
        <h1>
          Put the slider where <u>you think</u> the face looks <i>naturally </i>
          <strong>{{ trial.emotion }}</strong>
        </h1>
      </div>
      <ZoomableImage v-if="currentImage" :url="currentImage.url">
        <template v-slot:controls>
          <Slider
            v-model:value="selection"
            :min="0"
            :max="researchSetting.sliderSteps - 1"
            :step="1"
            :showSliderTooltip="false"
          />
        </template>
      </ZoomableImage>
    </div>

    <div v-else class="thank-you-message">
      <h1>Thank you for your participation!</h1>
      <p>
        The purpose of this study is to find the scalar value for emotion
        vectors of the StyleGAN FFHQ model such that it makes any face look
        natural for a certain emotion. Additionally, the data can be used to
        investigate the human perception of emotion.
      </p>
      <p>
        Should you want more information on the research project, please feel
        free to contact the student at
        <strong>m.makelis@student.ru.nl</strong>
      </p>
    </div>

    <div class="trial-controls">
      <div v-if="!completed" class="trial">
        <router-link :to="{ name: 'Research' }">
          <a-button type="default">
            <rollback-outlined />
            Exit
          </a-button>
        </router-link>
        <a-button type="primary" @click="next()">
          Next
          <caret-right-outlined />
        </a-button>
      </div>

      <div v-else class="final">
        <router-link :to="{ name: 'Research' }">
          <a-button type="primary">
            Finish
            <check-outlined />
          </a-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import {
  CaretRightOutlined,
  RollbackOutlined,
  CheckOutlined,
} from "@ant-design/icons-vue";
import ZoomableImage from "@/components/shared/image/ZoomableImage";
import Slider from "@/components/shared/controls/Slider";

import useResearchSettings from "@/modules/researchSettings";
import useResearchTrials from "@/modules/researchTrials";
import useCollectionImages from "@/modules/collectionImages";
import useTags from "@/modules/tags";

export default {
  name: "Trials",

  props: {
    session: {
      type: Object,
      required: true,
    },
  },

  async setup(props) {
    const { researchSettingsById } = useResearchSettings();
    const { getTrialsMetaInfoAsync, getTrialImagesAsync } = useResearchTrials();
    const { createTrialPickAsync } = useCollectionImages();
    const { researchTagsById, loadResearchTagsAsync } = useTags();

    const researchSetting =
      researchSettingsById[props.session.researchSettingId];

    const completed = ref(false);

    const trials = ref([]);

    const trial = ref();
    const selection = ref();
    const initialMultiplier = ref();

    const trialImages = ref();
    const currentImage = ref();

    watchEffect(() => {
      if (trialImages.value) {
        currentImage.value = trialImages.value[selection.value];
      }
    });

    trials.value = await getTrialsMetaInfoAsync(props.session.id);
    await next();

    await loadResearchTagsAsync();
    const tagsByEmotion = {};
    Object.values(researchTagsById).forEach((tag) => {
      tagsByEmotion[tag.name.toLowerCase()] = tag.id;
    });

    async function next() {
      if (trial.value) {
        await saveChoiceAsync();
      }
      if (trials.value.length === 0) {
        completed.value = true;
      } else {
        await nextTrialAsync();
      }
    }

    async function saveChoiceAsync() {
      const chosenImage = {
        imageId: currentImage.value.id,
        description: `Participant found this naturally ${trial.value.emotion}`,
        collectionId: props.session.participant.collectionId,
        tagsIds: [tagsByEmotion[trial.value.emotion]],
        trialNumber: props.session.progress + 1,
        initialMultiplier: initialMultiplier.value,
      };
      await createTrialPickAsync(chosenImage);
    }

    async function nextTrialAsync() {
      const randomTrial = Math.floor(Math.random() * trials.value.length);
      trial.value = trials.value[randomTrial];
      trials.value.splice(randomTrial, 1);
      trialImages.value = await getTrialImagesAsync(trial.value);
      const randomStart = Math.floor(
        Math.random() * researchSetting.sliderSteps
      );
      initialMultiplier.value = trialImages.value[randomStart].vectorMultiplier;
      selection.value = randomStart;
    }

    return {
      researchSetting,
      completed,
      trials,
      trial,
      selection,
      currentImage,
      next,
    };
  },

  components: {
    ZoomableImage,
    Slider,
    CaretRightOutlined,
    RollbackOutlined,
    CheckOutlined,
  },
};
</script>

<style lang="scss" scoped>
#trials {
  flex: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;

  .progress {
    width: 100%;
    position: absolute;
    top: -50px;
  }

  .trial {
    margin-bottom: 20px;
  }

  .thank-you-message {
    flex: 100%;
    justify-content: center;
    display: flex;
    flex-direction: column;

    p {
      text-align: justify;
    }
  }

  .trial-controls {
    margin-bottom: 20px;

    .trial {
      display: flex;
      justify-content: space-between;
    }

    .final {
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>