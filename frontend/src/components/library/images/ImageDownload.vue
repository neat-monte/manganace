<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Download image</span>
    </template>
    <a-button type="primary" shape="circle" @click="download(imageUrl)">
      <template v-slot:icon>
        <DownloadOutlined />
      </template>
    </a-button>
  </a-tooltip>
</template>

<script>
import { DownloadOutlined } from "@ant-design/icons-vue";
import download from "downloadjs";

export default {
  name: "ImageDownload",

  props: {
    imageUrl: String,
  },

  setup() {
    return {
      download,
    };
  },

  components: { DownloadOutlined },
};
</script>