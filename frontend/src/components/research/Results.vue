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
      title="Scalar choices of all participants plotted per emotion vector"
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

import useResearchData from "@/modules/researchData";
import { reactive, watchEffect } from "vue";

export default {
  name: "Results",

  props: {
    researchSettingId: {
      type: Number,
      required: true,
    },
  },

  async setup(props) {
    const { getExportCsvAsync, getResultsDataAsync } = useResearchData();

    async function downloadExportCsv() {
      const exportCsv = await getExportCsvAsync(props.researchSettingId);
      download(
        exportCsv,
        `export ${moment().format("DD-MM-YYYY HH-mm-ss")}.csv`
      );
    }

    const data = reactive([]);

    watchEffect(async () => {
      data.length = 0;
      const results = await getResultsDataAsync(props.researchSettingId);
      results.forEach((r) => data.push(r));
    });

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