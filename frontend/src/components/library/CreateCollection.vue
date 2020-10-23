<template>
  <div>
    <a-button shape="circle" @click="showModal">
      <template v-slot:icon>
        <PlusOutlined />
      </template>
    </a-button>

    <a-modal v-model:visible="visible" title="Basic Modal" @ok="handleOk">
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </a-modal>
  </div>
</template>

<script>
import { ref } from "vue";
import { PlusOutlined } from "@ant-design/icons-vue";

export default {
  name: "CreateCollection",

  setup() {
    const visible = ref();

    function showModal() {
      visible.value = true;
    }
    function handleOk() {
      visible.value = false;
    }

    return {
      handleOk,
      showModal,
      visible,
    };
  },

  components: { PlusOutlined },
};
</script>