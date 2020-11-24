<template>
  <div id="data-plot"></div>
</template>

<script>
import { onMounted } from "vue";
import Plotly from "plotly.js";

export default {
  name: "Boxplot",

  props: {
    data: Array,
    title: String,
  },

  setup(props) {
    onMounted(() => {
      Plotly.newPlot("data-plot", results, layout);
    });

    var results = [];

    for (var i = 0; i < props.data.length; i++) {
      var result = {
        type: "box",
        y: props.data[i].points,
        name: props.data[i].effect,
        boxpoints: "all",
        jitter: 0.1,
        whiskerwidth: 0.5,
        fillcolor: "cls",
        marker: {
          size: 2,
        },
        line: {
          width: 1,
        },
      };
      results.push(result);
    }

    var layout = {
      title: props.title,
      yaxis: {
        autorange: true,
        showgrid: true,
        zeroline: true,
        dtick: 2,
        gridcolor: "rgb(255, 255, 255)",
        gridwidth: 1,
        zerolinecolor: "rgb(255, 255, 255)",
        zerolinewidth: 2,
      },
      margin: {
        l: 40,
        r: 30,
        b: 80,
        t: 100,
      },
      paper_bgcolor: "rgb(243, 243, 243)",
      plot_bgcolor: "rgb(243, 243, 243)",
      showlegend: false,
    };
  },
};
</script>