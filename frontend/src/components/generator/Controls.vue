<template>
  <section id="controls">
    <div class="header">
      <span class="title">Controls</span>
    </div>
    <a-form layout="horizontal" class="request-form">
      <a-form-item>
        <div class="seed-multiplier">
          <div class="seed-input">
            <a-tooltip
              title="Enter a seed between 0 and 4294967296 (2³¹ - 1) inclusive"
            >
              <div class="label">Seed</div>
            </a-tooltip>
            <a-input
              :value="generateRequest.seed"
              @change="seedOnChange"
              :maxlength="10"
              :disabled="isGenerating"
              placeholder="Enter a seed of your choice"
            />
          </div>
          <div class="global-multiplier">
            <a-tooltip
              title="Scales all selected feature vector values by this amount"
            >
              <div class="label">Global multiplier</div>
            </a-tooltip>
            <a-input-number
              :value="globalMultiplier"
              :min="0.001"
              :step="0.001"
              @change="onGlobalMultiplierChange"
            />
          </div>
        </div>
      </a-form-item>
      <a-form-item v-for="vector in vectors" :key="vector.id">
        <Slider
          :label="vector.name"
          :tooltip="`Make the face look ${vector.effect}`"
          :enableInput="true"
          :min="vector.min"
          :max="vector.max"
          @update:value="vectorOnChange(vector.id, $event)"
        />
      </a-form-item>
    </a-form>
    <div class="controls">
      <a-button
        @click="generateAsync(generateRequest)"
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
import { ref, reactive } from "vue";

import { SyncOutlined } from "@ant-design/icons-vue";
import useGenerator from "@/modules/generator";
import Slider from "@/components/shared/controls/Slider";

export default {
  name: "Controls",

  async setup() {
    const {
      isGenerating,
      initGeneratorAsync,
      generateAsync,
      vectors,
    } = useGenerator();

    const globalMultiplier = ref(0.1);
    const prevGlobalMultiplier = ref(0.1);

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

    function onGlobalMultiplierChange(value) {
      if (isNaN(value) || value <= 0) {
        return;
      }
      globalMultiplier.value = value;
      generateRequest.vectors.forEach((vector) => {
        vector.multiplier =
          (vector.multiplier / prevGlobalMultiplier.value) * value;
      });
      prevGlobalMultiplier.value = value;
    }

    function vectorOnChange(id, value) {
      const vector = generateRequest.vectors.filter((e) => e.id === id)[0];

      if (vector && value > 0) {
        vector.multiplier = globalMultiplier.value * value;
      } else if (!vector && value > 0) {
        generateRequest.vectors.push({
          id: id,
          multiplier: globalMultiplier.value * value,
        });
      } else if (vector && value <= 0) {
        const index = generateRequest.vectors.indexOf(vector);
        generateRequest.vectors.splice(index, 1);
      }
    }

    await initGeneratorAsync();

    return {
      globalMultiplier,
      generateRequest,
      vectors,
      isGenerating,
      generateAsync,
      seedOnChange,
      vectorOnChange,
      onGlobalMultiplierChange,
    };
  },

  components: {
    Slider,
    SyncOutlined,
  },
};
</script>

<style lang="scss" scoped>
#controls {
  padding: 0 20px 20px 20px;
  display: flex;
  flex-direction: column;

  .request-form {
    flex: 1;

    .seed-multiplier {
      display: flex;
      justify-content: space-between;

      .seed-input,
      .global-multiplier {
        flex: 1;
        display: flex;
        align-items: center;
      }

      .global-multiplier {
        justify-content: flex-end;
      }
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