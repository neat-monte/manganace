<template>
  <div class="slider">
    <a-tooltip v-if="tooltip && label" placement="top" :title="tooltip">
      <div class="label">{{ label }}</div>
    </a-tooltip>
    <div v-if="!tooltip && label" class="label">{{ label }}</div>
    <a-slider
      v-model:value="value"
      :min="min"
      :max="max"
      :step="step"
      @afterChange="onValueChange"
    />
    <a-input-number
      v-if="enableInput"
      :value="value"
      :min="min"
      :max="max"
      :step="step"
      @change="onValueChange"
    />
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Slider",

  props: {
    label: {
      type: String,
      default: null,
    },
    tooltip: {
      type: String,
      default: null,
    },
    enableInput: {
      type: Boolean,
      default: false,
    },
    min: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 1,
    },
    step: {
      type: Number,
      default: 0.01,
    },
  },

  emits: ["change"],

  setup(props, context) {
    const value = ref(props.min);

    function onValueChange(newValue) {
      const onlyFloat = /^\d+(\.\d+)?$/;
      if (!isNaN(newValue) && onlyFloat.test(newValue)) {
        const num = Number(newValue);
        if (props.min <= num && num <= props.max) {
          value.value = num;
          context.emit("change", num);
        }
      }
    }

    return {
      value,
      onValueChange,
    };
  },
};
</script>

<style lang="scss" scoped>
.slider {
  display: flex;
  align-items: center;

  .label {
    margin-left: 5px;
    margin-right: 5px;
    text-transform: capitalize;
    width: 100px;

    &.ant-tooltip-open {
      cursor: help;
    }
  }

  .ant-slider {
    flex: 1;
  }

  .ant-input-number {
    margin-left: 5px;
  }
}
</style>