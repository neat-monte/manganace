<template>
  <div id="research-results">
    <div class="controls">
      <a-button type="primary" @click="downloadExportCsv()">
        Export data
      </a-button>
    </div>
    <div id="data-plot"></div>
  </div>
</template>

<script>
import { onMounted } from "vue";
import download from "downloadjs";
import Plotly from "plotly.js";

import useResearch from "@/modules/research";

export default {
  name: "Results",

  async setup() {
    const { getExportCsvAsync, getResultsDataAsync } = useResearch();

    async function downloadExportCsv() {
      const exportCsv = await getExportCsvAsync();
      download(exportCsv, `export.csv`);
    }

    onMounted(() => {
      Plotly.newPlot("data-plot", results, layout);
    });

    const data = await getResultsDataAsync();

    var results = [];

    for (var i = 0; i < data.length; i++) {
      var result = {
        type: "box",
        y: data[i].points,
        name: data[i].effect,
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
      title: "Chosen multipliers for each vector of all the participants",
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
      downloadExportCsv,
    };
  },
};
</script>

<style lang="scss" scoped>
#research-results {
  .controls {
    text-align: right;
    margin-right: 10px;
    margin-bottom: 20px;
  }
}

@include tablet {
  #research-results {
    margin: 0;

    .controls {
      margin-right: 0;
    }
  }
}
</style>