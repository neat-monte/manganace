<template>
  <div class="collection-card">
    <span class="sm-title">
      {{ collection.name }}
    </span>
    <div class="information">
      <p>{{ collection.description }}</p>
      <a-descriptions size="small" :column="1">
        <a-descriptions-item label="Created">
          {{ collection.created }}
        </a-descriptions-item>
        <a-descriptions-item v-if="collection.updated" label="Updated">
          {{ collection.updated }}
        </a-descriptions-item>
      </a-descriptions>
    </div>
    <div class="card-controls">
      <CollectionDelete :collectionId="collection.id" />
      <CollectionUpdate :collection="collection" />
      <Images :collectionId="collection.id" />
    </div>
  </div>
</template>

<script>
import Images from "@/components/library/Images";
import CollectionUpdate from "@/components/shared/modals/collection/CollectionUpdate";
import CollectionDelete from "@/components/shared/modals/collection/CollectionDelete";

export default {
  name: "CollectionCard",
  props: {
    collection: Object,
  },

  components: {
    Images,
    CollectionUpdate,
    CollectionDelete,
  },
};
</script>

<style lang="scss" scoped>
.collection-card {
  position: relative;
  overflow: hidden;
  border: 1px solid $darkness-20;
  background: $darkness-05;
  border-radius: 2px;
  padding: 10px 20px;

  .information {
    margin: 10px 0;
    text-align: left;
  }

  .card-controls {
    position: absolute;
    background: $filler-80;
    left: 0;
    bottom: -100%;
    transition: all 0.2s ease;
    visibility: hidden;
    padding: 10px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    width: 100%;
  }

  &:hover {
    .card-controls {
      bottom: 0;
      visibility: visible;
    }
  }
}
</style>