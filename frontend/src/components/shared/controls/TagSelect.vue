<template>
  <div class="tag-select">
    <a-select
      @change="handleChange"
      :value="modelValue"
      mode="multiple"
      :placeholder="placeholder"
      :allowClear="true"
      optionLabelProp="key"
      optionFilterProp="key"
      notFoundContent="No such tag exists, create new!"
    >
      <a-select-option
        v-for="[id, tag] of Object.entries(tagsById)"
        :key="tag.name"
        :value="Number(id)"
      >
        {{ tag.name }}
      </a-select-option>
    </a-select>
    <TagCreate v-if="showCreate" />
  </div>
</template>

<script>
import useTags from "@/modules/tags";
import TagCreate from "@/components/shared/modals/tag/TagCreate";

export default {
  name: "TagSelect",

  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    placeholder: {
      type: String,
      default: "Choose tags",
    },
    showCreate: {
      type: Boolean,
      default: true,
    },
  },

  emits: ["update:modelValue"],

  async setup(props, context) {
    const { tagsById, loadTagsAsync } = useTags();

    function handleChange(value) {
      context.emit("update:modelValue", value);
    }

    await loadTagsAsync();

    return {
      handleChange,
      tagsById,
    };
  },

  components: {
    TagCreate,
  },
};
</script>

<style lang="scss" scoped>
.tag-select {
  display: flex;
  width: 100%;

  .ant-select {
    width: 100%;

    .ant-select-selection {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }
  }
}
</style>