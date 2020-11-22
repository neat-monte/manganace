<template>
  <h2>Results</h2>
  <div id="plot"></div>
</template>

<script>
import { onMounted } from "vue";
import Plotly from "plotly.js";

export default {
  name: "Results",

  setup() {
    var y0 = [];
    var y1 = [];
    for (var i = 0; i < 50; i++) {
      y0[i] = Math.random();
      y1[i] = Math.random() + 1;
    }

    var trace1 = {
      y: y0,
      type: "box",
    };

    var trace2 = {
      y: y1,
      type: "box",
    };

    var data = [trace1, trace2];

    onMounted(() => {
      Plotly.newPlot("plot", data);
    });
  },

  components: {},
};
</script>