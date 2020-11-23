<template>
  <section id="controls">
    <div class="header">
      <span class="title">Controls</span>
    </div>
    <a-form class="request-form">
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
          @update:value="vectorOnChange(vector.id, $event)"
        />
      </a-form-item>
    </a-form>
    <div class="controls">
      <a-button @click="clearGenerateRequest" type="secondary">
        Clear
        <clear-outlined />
      </a-button>
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
import { reactive } from "vue";

import { SyncOutlined, ClearOutlined } from "@ant-design/icons-vue";
import useGenerator from "@/modules/generator";
import Slider from "@/components/shared/Slider";

export default {
  name: "Controls",

  async setup() {
    const {
      isGenerating,
      initGeneratorAsync,
      generateAsync,
      vectors,
    } = useGenerator();

    const generateRequest = reactive({
      seed: "",
      vectors: [],
    });

    function clearGenerateRequest() {
      generateRequest.seed = "";
      generateRequest.vectors = [];
    }

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

    await initGeneratorAsync();

    return {
      generateRequest,
      clearGenerateRequest,
      vectors,
      isGenerating,
      generateAsync,
      seedOnChange,
      vectorOnChange,
    };
  },

  components: {
    Slider,
    SyncOutlined,
    ClearOutlined,
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