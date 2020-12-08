<template>
  <a-button
    v-if="buttonText"
    type="primary"
    :disabled="!imageUrl"
    @click="download(imageUrl)"
  >
    {{ buttonText }}
    <download-outlined />
  </a-button>

  <a-tooltip v-else placement="top" title="Download image">
    <a-button type="primary" :disabled="!imageUrl" @click="download(imageUrl)">
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
    buttonText: {
      type: String,
      default: null,
    },
  },

  setup() {
    return {
      download,
    };
  },

  components: { DownloadOutlined },
};
</script>