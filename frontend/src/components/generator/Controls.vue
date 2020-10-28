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
            :disabled="generating"
            placeholder="Enter a seed"
          />
        </a-form-item>
      </a-form>
      <a-button
        @click="generate(generateRequest)"
        :disabled="generating"
        type="primary"
      >
        Generate
      </a-button>
    </div>
  </section>
</template>

<script>
import { reactive } from "vue";

import useGenerator from "@/modules/useGenerator";

export default {
  name: "Controls",

  async setup() {
    const { generating, initGenerator, generate } = useGenerator();
    await initGenerator();

    const generateRequest = reactive({
      seed: "",
    });

    function seedOnChange(e) {
      const { value } = e.target;
      const onlyInt = /^-?[1-9]([0-9]*)?$/;
      if ((!isNaN(value) && onlyInt.test(value)) || value === "") {
        generateRequest.seed = value;
      }
    }

    return {
      generateRequest,
      generating,
      generate,
      seedOnChange,
    };
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