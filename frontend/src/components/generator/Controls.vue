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
        <a-form-item v-for="vector in vectors" :key="vector.id">
          <Slider
            :label="vector.name"
            :tooltip="`Make the face look ${vector.effect}`"
            :enableInput="true"
            :min="vector.min"
            :max="vector.max"
            @change="vectorOnChange(vector.id, $event)"
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
    const { isGenerating, initGenerator, generate, vectors } = useGenerator();

    const generateRequest = reactive({
      seed: "",
      vectors: [],
    });

    function seedOnChange(e) {
      const { value } = e.target;
      const onlyInt = /^([1-9]\d*|0)$/;
      if ((!isNaN(value) && onlyInt.test(value)) || value === "") {
        generateRequest.seed = value;
      }
    }

    function vectorOnChange(id, value) {
      const vector = generateRequest.vectors.filter((e) => e.id === id)[0];

      if (vector && value > 0) {
        vector.multiplier = value;
      } else if (!vector && value > 0) {
        generateRequest.vectors.push({
          id: id,
          multiplier: value,
        });
      } else if (vector && value <= 0) {
        const index = generateRequest.vectors.indexOf(vector);
        generateRequest.vectors.splice(index, 1);
      }
    }

    await initGenerator();

    return {
      vectors,
      generateRequest,
      isGenerating,
      generate,
      seedOnChange,
      vectorOnChange,
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