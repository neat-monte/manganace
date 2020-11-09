<template>
  <section id="controls">
    <div class="wrapper">
      <div class="header">
        <span class="title">Controls</span>
      </div>
      <a-form>
        <a-form-item>
          <a-input
            :value="generateRequest.seed"
            @change="seedOnChange"
            :maxlength="10"
            :disabled="isGenerating"
            placeholder="Enter a seed"
          />
        </a-form-item>
        <a-form-item v-for="emotion in emotions" :key="emotion.id">
          <Slider
            :label="emotion.name"
            :enableInput="true"
            :min="emotion.min"
            :max="emotion.max"
            @change="emotionOnChange(emotion.id, $event)"
          />
        </a-form-item>
      </a-form>
      <a-button
        @click="generate(generateRequest)"
        :disabled="isGenerating"
        type="primary"
      >
        Generate
      </a-button>
    </div>
  </section>
</template>

<script>
import { reactive } from "vue";
import Slider from "@/components/shared/Slider";

import useGenerator from "@/modules/generator";

export default {
  name: "Controls",

  async setup() {
    const { isGenerating, initGenerator, generate, emotions } = useGenerator();

    const generateRequest = reactive({
      seed: "",
      emotions: [],
    });

    function seedOnChange(e) {
      const { value } = e.target;
      const onlyInt = /^([1-9]\d*|0)$/;
      if ((!isNaN(value) && onlyInt.test(value)) || value === "") {
        generateRequest.seed = value;
      }
    }

    function emotionOnChange(id, value) {
      const emotion = generateRequest.emotions.filter((e) => e.id === id)[0];

      if (emotion && value > 0) {
        emotion.multiplier = value;
      } else if (!emotion && value > 0) {
        generateRequest.emotions.push({
          id: id,
          multiplier: value,
        });
      } else if (emotion && value <= 0) {
        const index = generateRequest.emotions.indexOf(emotion);
        generateRequest.emotions.splice(index, 1);
      }
    }

    await initGenerator();

    return {
      emotions,
      generateRequest,
      isGenerating,
      generate,
      seedOnChange,
      emotionOnChange,
    };
  },

  components: {
    Slider,
  },
};
</script>

<style lang="scss" scoped>
#controls {
  padding: 20px;
}

@include tablet {
  #controls {
    border-radius: 2px;
    box-shadow: $box-double-shadow;
    margin-bottom: 20px;
  }
}
</style>