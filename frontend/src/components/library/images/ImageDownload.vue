<template>
  <a-button type="primary" shape="circle" @click="download(imageUrl)">
    <template v-slot:icon>
      <DownloadOutlined />
    </template>
  </a-button>
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