<template>
  <div id="research-results">
    <div class="controls">
      <a-button type="primary" @click="downloadExportCsv()">
        Export data
        <export-outlined />
      </a-button>
    </div>
    <Boxplot
      v-if="data.length > 0"
      :data="data"
      title="Chosen multipliers for each vector of all the participants"
    />
    <Empty v-else />
  </div>
</template>

<script>
import download from "downloadjs";
import moment from "moment";

import { ExportOutlined } from "@ant-design/icons-vue";
import Boxplot from "@/components/shared/infographics/Boxplot";
import Empty from "@/components/shared/display/Empty";

import useResearch from "@/modules/research";

export default {
  name: "Results",

  async setup() {
    const { getExportCsvAsync, getResultsDataAsync } = useResearch();

    async function downloadExportCsv() {
      const exportCsv = await getExportCsvAsync();
      download(
        exportCsv,
        `export ${moment().format("DD-MM-YYYY HH-mm-ss")}.csv`
      );
    }

    const data = await getResultsDataAsync();

    return {
      data,
      downloadExportCsv,
    };
  },

  components: {
    Boxplot,
    ExportOutlined,
    Empty,
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