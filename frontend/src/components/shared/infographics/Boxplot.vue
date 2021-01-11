<template>
  <div :id="plotId"></div>
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
    const plotId = `data-plot-${makeId(8)}`;

    onMounted(() => {
      const plot = getPlotData();
      Plotly.newPlot(plotId, plot.results, plot.layout);
    });

    function getPlotData() {
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
          boxmean: "sd",
          notched: true,
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
      return {
        results,
        layout,
      };
    }

    function makeId(length) {
      var result = "";
      var characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      var charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    }

    return {
      plotId,
    };
  },
};
</script>