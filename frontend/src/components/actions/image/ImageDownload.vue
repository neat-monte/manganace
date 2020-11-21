<template>
  <a-tooltip placement="top">
    <template v-slot:title>
      <span>Download image</span>
    </template>
    <a-button @click="download(imageUrl)" :disabled="!imageUrl" type="primary">
      <template v-slot:icon>
        <download-outlined />
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