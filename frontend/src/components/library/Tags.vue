<template>
  <div id="tags">
    <div class="tags-header">
      <span class="title">Tags</span>
      <div class="controls">
        <TagCreate />
      </div>
    </div>
    <a-list :grid="{ gutter: 20, xs: 2, md: 2, lg: 3, xl: 4, xxl: 6 }">
      <a-list-item v-for="tag in tags" :key="tag.id">
        <TagCard :tag="tag" />
      </a-list-item>
    </a-list>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import TagCreate from "@/components/actions/tag/TagCreate";
import TagCard from "@/components/library/TagCard";

import useTags from "@/modules/tags";

export default {
  name: "Tags",

  async setup() {
    const { tagsById, loadTagsAsync } = useTags();
    const tags = ref([]);

    watchEffect(() => {
      tags.value = Object.values(tagsById);
    });

    await loadTagsAsync();

    return {
      tags,
    };
  },

  components: {
    TagCreate,
    TagCard,
  },
};
</script>

<style lang="scss" scoped>
#tags {
  display: initial;
  padding: 0 20px 10px 20px;
  height: 100%;

  .tags-header {
    display: flex;
    position: relative;
    margin: 8px 16px;

    .title {
      width: 100%;
      margin: 0;
      padding: 10px;
    }

    .controls {
      position: absolute;
      align-self: center;
      right: 0;
    }
  }
}

@include tablet {
  #tags {
    padding: 0 20px 10px 20px;
  }
}
</style>