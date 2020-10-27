<template>
  <a-button type="primary" shape="circle" @click="download()">
    <template v-slot:icon>
      <DownloadOutlined />
    </template>
  </a-button>
</template>

<script>
import { DownloadOutlined } from "@ant-design/icons-vue";

export default {
  name: "ImageDownload",

  setup() {
    function download() {}

    return {
      download,
    };
  },

  components: { DownloadOutlined },
};
</script>