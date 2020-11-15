<template>
  <div id="tags">
    <div class="tags-header">
      <span class="title">Tags manager</span>
      <div class="controls">
        <TagCreate />
      </div>
    </div>
    <a-list bordered>
      <a-list-item v-for="tag in tags" :key="tag.id">
        <span>{{ tag.name }}</span>
        <template v-slot:actions>
          <TagUpdate :tag="tag" />
          <TagDelete :tagId="tag.id" />
        </template>
      </a-list-item>
    </a-list>
  </div>
</template>

<script>
import TagCreate from "@/components/actions/tag/TagCreate";
import TagUpdate from "@/components/actions/tag/TagUpdate";
import TagDelete from "@/components/actions/tag/TagDelete";

import useTags from "@/modules/tags";
import { ref, watchEffect } from "vue";

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
    TagUpdate,
    TagDelete,
  },
};
</script>

<style lang="scss" scoped>
#tags {
  width: 100vw;

  .tags-header {
    padding: 20px;
    display: flex;
    position: relative;
    margin: 0 24px;

    .title {
      width: 100%;
    }

    .controls {
      position: absolute;
      align-self: center;
      right: 10px;
    }
  }
}
</style>