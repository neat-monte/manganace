<template>
  <section id="controls">
    <div class="controls-header">
      <span class="title">Controls</span>
    </div>
    <a-form>
      <a-form-item>
        <a-input
          :value="generateRequest.seed"
          @change="seedOnChange"
          :maxlength="10"
          placeholder="Enter a seed"
          :disabled="generating"
        />
      </a-form-item>
    </a-form>
    <a-button @click="generate" type="primary" :disabled="generating">
      Generate
    </a-button>
  </section>
</template>

<script>
import { reactive, ref } from "vue";
import useGenerator from "@/modules/useGenerator";

export default {
  name: "Controls",

  async setup() {
    const { initGenerator, generateImage } = useGenerator();
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

    const generating = ref(false);
    async function generate() {
      generating.value = true;
      await generateImage(generateRequest);
      generating.value = false;
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
  flex: 1;
  order: -1;
}

@include sm-desktop {
  #controls {
    margin-right: 10px;
  }
}

@include lg-desktop {
  #controls {
    margin-right: 20px;
  }
}
</style>