<template>
  <div class="trial">
    <p>Current: {{ trial }}</p>
  </div>
</template>

<script>
import { ref } from "vue";

import useResearch from "@/modules/research";
import { watchEffect } from "vue";

export default {
  name: "Trial",

  props: {
    trial: Object,
  },

  emits: ["change"],

  setup(props) {
    const { getTrialImagesAsync } = useResearch();
    const images = ref([]);

    watchEffect(async () => {
      if (props.trial) {
        images.value = await getTrialImagesAsync(props.trial);
      }
    });

    return {
      images,
    };
  },

  components: {},
};
</script>