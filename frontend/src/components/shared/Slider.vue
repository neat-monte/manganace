<template>
  <div class="slider">
    <a-tooltip v-if="tooltip && label" placement="top" :title="tooltip">
      <div class="label">{{ label }}</div>
    </a-tooltip>
    <div v-if="!tooltip && label" class="label">{{ label }}</div>
    <a-slider
      :value="internalValue"
      :min="min"
      :max="max"
      :step="step"
      :tooltipVisible="showSliderTooltip"
      @change="onValueChange"
    />
    <a-input-number
      v-if="enableInput"
      :value="internalValue"
      :min="min"
      :max="max"
      :step="step"
      @change="onValueChange"
    />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

export default {
  name: "Slider",

  props: {
    value: {
      type: Number,
      default: 0,
    },
    showSliderTooltip: {
      type: Boolean,
      default: undefined,
    },
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

  emits: ["update:value", "change"],

  setup(props, context) {
    const internalValue = ref();

    watchEffect(() => {
      internalValue.value = props.value;
    });

    function onValueChange(newValue) {
      const onlyFloat = /^\d+(\.\d+)?$/;
      if (!isNaN(newValue) && onlyFloat.test(newValue)) {
        const num = Number(newValue);
        if (props.min <= num && num <= props.max) {
          internalValue.value = num;
          context.emit("change", num);
          context.emit("update:value", num);
        }
      }
    }

    return {
      onValueChange,
      internalValue,
    };
  },
};
</script>

<style lang="scss" scoped>
.slider {
  width: 100%;
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