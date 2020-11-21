<template>
  <div class="tag-card">
    <div class="tag-inner">
      <span class="tag-title">
        {{ tag.name }}
      </span>
      <div class="card-controls">
        <TagUpdate :tag="tag" />
        <TagDelete
          v-if="tag.forResearch"
          :disabled="true"
          tooltip="Cannot delete - used for research"
          :tagId="tag.id"
        />
        <TagDelete v-else :tagId="tag.id" />
      </div>
    </div>
  </div>
</template>

<script>
import TagUpdate from "@/components/actions/tag/TagUpdate";
import TagDelete from "@/components/actions/tag/TagDelete";

export default {
  name: "TagCard",

  props: {
    tag: Object,
  },

  components: {
    TagUpdate,
    TagDelete,
  },
};
</script>

<style lang="scss" scoped>
.tag-card {
  padding: 0 8px;
  min-height: 40px;

  .tag-inner {
    position: relative;
    overflow: hidden;
    border: 1px solid $darkness-20;
    background: $darkness-05;
    border-radius: 2px;
    padding: 10px 40px;

    .tag-title {
      font-size: 1rem;
      font-weight: bold;
    }

    .card-controls {
      position: absolute;
      background: $filler-35;
      bottom: -40px;
      left: 0;
      transition: all 0.2s ease;
      height: 100%;
      visibility: hidden;
      width: 100%;
      padding: 0 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  &:hover {
    .tag-inner {
      .card-controls {
        bottom: 0;
        visibility: visible;
      }
    }
  }
}
</style>