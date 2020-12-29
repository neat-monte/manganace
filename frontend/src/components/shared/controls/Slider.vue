<template>
  <div class="slider">
    <a-tooltip v-if="tooltip && label" placement="top" :title="tooltip">
      <div class="label">{{ label }}</div>
    </a-tooltip>
    <div v-if="!tooltip && label" class="label">{{ label }}</div>
    <div v-if="enableReset" class="reload">
      <ReloadOutlined @click="onValueChange(0)" />
    </div>
    <a-slider
      :value="value"
      :min="min"
      :max="max"
      :step="step"
      :tooltipVisible="showSliderTooltip"
      :disabled="disabled"
      @change="onValueChange"
    />
    <a-input-number
      v-if="enableInput"
      :value="value"
      :min="min"
      :max="max"
      :step="step"
      :disabled="disabled"
      @change="onValueChange"
    />
  </div>
</template>

<script>
import { ReloadOutlined } from "@ant-design/icons-vue";

export default {
  name: "Slider",

  props: {
    value: {
      type: Number,
      default: 0,
    },
    enableInput: {
      type: Boolean,
      default: false,
    },
    enableReset: {
      type: Boolean,
      default: false,
    },
    showSliderTooltip: {
      type: Boolean,
      default: false,
    },
    min: {
      type: Number,
      default: -1,
    },
    max: {
      type: Number,
      default: 1,
    },
    step: {
      type: Number,
      default: 0.01,
    },
    label: {
      type: String,
      default: null,
    },
    tooltip: {
      type: String,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },

  setup(props, context) {
    function onValueChange(newValue) {
      if (props.disabled) {
        return;
      }
      const onlyFloat = /^[-+]?\d+(\.\d+)?$/;
      if (!isNaN(newValue) && onlyFloat.test(newValue)) {
        const num = Number(newValue);
        if (props.min <= num && num <= props.max) {
          context.emit("update:value", num);
        }
      }
    }

    return {
      onValueChange,
    };
  },

  components: {
    ReloadOutlined,
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

  .reload {
    color: $primary;
    margin-right: 5px;
  }
}
</style>