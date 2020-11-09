<template>
  <div class="tag-select">
    <a-select
      @change="handleChange"
      v-model:value="selectedTags"
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
    <TagCreate v-if="showCreate" :isAddon="true" />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import useTags from "@/modules/tags";
import TagCreate from "@/components/actions/tag/TagCreate";

export default {
  name: "TagSelect",

  props: {
    initialTags: {
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

  emits: ["tag-id-set"],

  async setup(props, context) {
    const { tagsById, loadTags } = useTags();
    const selectedTags = ref([]);

    watchEffect(() => {
      selectedTags.value = props.initialTags;
    });

    function handleChange(value) {
      context.emit("tag-id-set", value);
    }

    await loadTags();

    return {
      selectedTags,
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