<template>
  <section id="tags">
    <div class="tags-header">
      <span class="title">Tags</span>
      <div class="controls">
        <TagCreate />
      </div>
    </div>
    <a-list :grid="{ gutter: 20, xs: 2, md: 1 }" :data-source="tags">
      <template #renderItem="{ item, index }">
        <a-list-item :key="index">
          <TagCard :tag="item" />
        </a-list-item>
      </template>
    </a-list>
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";

import TagCreate from "@/components/shared/modals/tag/TagCreate";
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
    margin: 8px 0;

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
    padding: 0 0 10px 20px;
  }
}
</style>