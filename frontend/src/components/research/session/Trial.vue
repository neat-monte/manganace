<template>
  <div class="trial">
    <p>Trial: {{ trial }}</p>
    <p v-if="currentImage">Image: {{ currentImage }}</p>
    <div v-if="currentImage">
      <img :src="currentImage.url" />
    </div>
    <Slider
      :min="0"
      :max="currentSession.sliderSteps"
      :step="1"
      @change="swapImage"
    />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import Slider from "@/components/shared/Slider";

import useResearch from "@/modules/research";

export default {
  name: "Trial",

  props: {
    trial: Object,
  },

  emits: ["change"],

  setup(props) {
    const { currentSession, getTrialImagesAsync } = useResearch();
    const images = ref([]);
    const currentImage = ref({});

    watchEffect(async () => {
      if (props.trial) {
        images.value = await getTrialImagesAsync(props.trial);
        const randomIndex = Math.floor(Math.random() * images.value.length);
        currentImage.value = images.value[randomIndex];
      }
    });

    function swapImage(index) {
      currentImage.value = images.value[index];
    }

    return {
      currentSession,
      images,
      swapImage,
      currentImage,
    };
  },

  components: {
    Slider,
  },
};
</script>