<template>
  <section id="controls">
    <div class="header">
      <span class="title">Controls</span>
    </div>
    <a-form class="request-form" layout="horizontal">
      <a-form-item>
        <div class="inline">
          <div class="item">
            <a-tooltip
              title="Enter a seed between 0 and 2147483647 (2³¹ - 1) inclusive"
            >
              <div class="label">Seed</div>
            </a-tooltip>
            <div class="random-seed">
              <question-outlined @click="randomSeed" />
            </div>
            <a-input
              :value="generateRequest.seed"
              @change="seedOnChange"
              :maxlength="10"
              :disabled="isGenerating"
              placeholder="Enter a seed of your choice"
            />
          </div>
          <div class="item end-item">
            <a-tooltip
              title="Scales all selected feature vector values by this amount. You can see this as a radius limit in the latent space."
            >
              <div class="label">Global multiplier</div>
            </a-tooltip>
            <a-input-number
              :value="globalMultiplier"
              :min="0.001"
              :step="0.001"
              :disabled="isGenerating"
              @change="onGlobalMultiplierChange"
            />
          </div>
        </div>
      </a-form-item>
      <a-form-item v-for="vector in vectors" :key="vector.id">
        <Slider
          v-model:value="vectorValues[vector.id]"
          @update:value="vectorOnChange(vector.id, $event)"
          :min="sliderOpt.min"
          :max="sliderOpt.max"
          :enableReset="true"
          :enableInput="true"
          :label="vector.name"
          :tooltip="`Make the face look ${vector.effect}`"
          :disabled="isGenerating"
        />
      </a-form-item>
      <a-form-item>
        <div class="inline inline-center">
          <div class="item">
            <a-tooltip title="Minimum value of a slider">
              <div class="label">Slider min</div>
            </a-tooltip>
            <a-input-number
              v-model:value="sliderOpt.min"
              :step="0.1"
              :disabled="isGenerating"
            />
          </div>
          <div class="item">
            <a-input-number
              v-model:value="sliderOpt.max"
              :step="0.1"
              :disabled="isGenerating"
            />
            <a-tooltip title="Maximum value of a slider">
              <div class="label">Slider max</div>
            </a-tooltip>
          </div>
        </div>
      </a-form-item>
    </a-form>
    <div class="controls">
      <a-button @click="resetToDefaults" :disabled="isGenerating">
        Reset to defaults
        <clear-outlined />
      </a-button>
      <a-button @click="resetSliders" :disabled="isGenerating">
        Reset all sliders
        <reload-outlined />
      </a-button>
      <a-button
        @click="generate"
        :disabled="isGenerating || !generateRequest.seed"
        type="primary"
      >
        Generate
        <sync-outlined />
      </a-button>
    </div>
  </section>
</template>

<script>
import { ref, reactive, watchEffect } from "vue";

import {
  SyncOutlined,
  ReloadOutlined,
  QuestionOutlined,
  ClearOutlined,
} from "@ant-design/icons-vue";
import useGenerator from "@/modules/generator";
import Slider from "@/components/shared/controls/Slider";

export default {
  name: "Controls",

  props: {
    sessionId: {
      type: Number,
      required: true,
    },
  },

  async setup(props) {
    const {
      isGenerating,
      initGeneratorAsync,
      generateAsync,
      vectors,
      currentImage,
    } = useGenerator();

    const globalMultiplier = ref(0.2);
    const prevGlobalMultiplier = ref(0.2);

    const sliderOpt = reactive({
      min: -1,
      max: 1,
    });

    const vectorValues = reactive({});
    watchEffect(() => {
      Object.values(vectors).forEach((v) => (vectorValues[v.id] = 0));
    });

    const generateRequest = reactive({
      seed: "",
      vectors: [],
      sessionId: props.sessionId,
    });

    const lastMappedImageId = ref();

    watchEffect(() => {
      if (currentImage.id && lastMappedImageId.value !== currentImage.id) {
        resetSliders();

        const copy = JSON.parse(JSON.stringify(currentImage));
        lastMappedImageId.value = copy.id;

        generateRequest.seed = copy.seed;
        generateRequest.vectors = copy.vectors;

        copy.vectors.forEach((v) => {
          let vectorValue = v.multiplier / globalMultiplier.value;
          vectorValue = vectorValue.toPrecision(5);

          if (vectorValue > sliderOpt.max) {
            sliderOpt.max = vectorValue;
          } else if (vectorValue < sliderOpt.min) {
            sliderOpt.min = vectorValue;
          }

          vectorValues[v.id] = Number(vectorValue);
        });
      }
    });

    function randomSeed() {
      const min = 0; // inclusive
      const max = 2 ** 31; // exclusive
      generateRequest.seed = Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function seedOnChange(e) {
      const { value } = e.target;
      const onlyInt = /^([1-9]\d*|0)$/;
      if (
        (!isNaN(value) && onlyInt.test(value) && value < 2 ** 31) ||
        value === ""
      ) {
        generateRequest.seed = value;
      }
    }

    function onGlobalMultiplierChange(value) {
      if (isNaN(value) || value <= 0) {
        return;
      }
      globalMultiplier.value = value;
      generateRequest.vectors.forEach((vector) => {
        vector.multiplier = (
          (vector.multiplier / prevGlobalMultiplier.value) *
          value
        ).toPrecision(5);
      });
      prevGlobalMultiplier.value = value;
    }

    function vectorOnChange(id, value) {
      const vector = generateRequest.vectors.filter((e) => e.id === id)[0];

      if (vector && value == 0) {
        const index = generateRequest.vectors.indexOf(vector);
        generateRequest.vectors.splice(index, 1);
      } else if (vector) {
        vector.multiplier = (globalMultiplier.value * value).toPrecision(5);
      } else if (!vector) {
        generateRequest.vectors.push({
          id: id,
          multiplier: (globalMultiplier.value * value).toPrecision(5),
        });
      }
    }

    function resetSliders() {
      generateRequest.vectors = [];
      Object.keys(vectorValues).forEach((k) => (vectorValues[k] = 0));
    }

    function resetToDefaults() {
      globalMultiplier.value = 0.2;
      sliderOpt.min = -1;
      sliderOpt.max = 1;
      generateRequest.seed = "";
      resetSliders();
    }

    async function generate() {
      await generateAsync(generateRequest);
    }

    await initGeneratorAsync();

    return {
      resetToDefaults,
      resetSliders,
      generate,
      globalMultiplier,
      generateRequest,
      vectors,
      vectorValues,
      isGenerating,
      generateAsync,
      seedOnChange,
      vectorOnChange,
      onGlobalMultiplierChange,
      sliderOpt,
      randomSeed,
      currentImage,
    };
  },

  components: {
    Slider,
    SyncOutlined,
    ReloadOutlined,
    QuestionOutlined,
    ClearOutlined,
  },
};
</script>

<style lang="scss" scoped>
#controls {
  padding: 0 20px 20px 20px;
  display: flex;
  flex-direction: column;

  .header {
    margin-bottom: 20px;
  }

  .request-form {
    flex: 1;

    .inline {
      display: flex;
      justify-content: space-between;

      .item {
        flex: 1;
        display: flex;
        align-items: center;
      }

      .end-item {
        justify-content: flex-end;
      }

      &.inline-center {
        .item:first-child {
          justify-content: flex-end;
        }

        .item:last-child {
          justify-content: flex-start;
          text-align: end;
        }
      }
    }

    .random-seed {
      color: $primary;
      margin-right: 5px;
    }

    .label {
      margin-left: 5px;
      margin-right: 5px;
      min-width: 100px;

      &.ant-tooltip-open {
        cursor: help;
      }
    }
  }

  .controls {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 20px 0;
  }
}

@include sm-desktop {
  #controls {
    padding: 0 0 20px 20px;
  }
}
</style>