<template>
  <div class="tag-card">
    <span class="sm-title">
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
</template>

<script>
import TagUpdate from "@/components/shared/modals/tag/TagUpdate";
import TagDelete from "@/components/shared/modals/tag/TagDelete";

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
  position: relative;
  overflow: hidden;
  border: 1px solid $darkness-20;
  background: $darkness-05;
  border-radius: 2px;
  padding: 10px 40px;

  .card-controls {
    position: absolute;
    background: $filler-35;
    bottom: -100%;
    left: 0;
    height: 100%;
    width: 100%;
    visibility: hidden;
    padding: 0 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
  }

  &:hover {
    .card-controls {
      bottom: 0;
      visibility: visible;
    }
  }
}
</style>