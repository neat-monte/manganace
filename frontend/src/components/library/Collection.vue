<template>
  <div class="collection">
    <p>{{ collection.description }}</p>
    <a-descriptions size="small" :column="1">
      <a-descriptions-item label="Created">
        {{ collection.created }}
      </a-descriptions-item>
      <a-descriptions-item v-if="collection.updated" label="Updated">
        {{ collection.updated }}
      </a-descriptions-item>
    </a-descriptions>
    <div class="controls">
      <CollectionDelete :collectionId="collection.id" />
      <CollectionUpdate :collection="collection" />
    </div>
  </div>
</template>

<script>
import CollectionUpdate from "@/components/actions/collection/CollectionUpdate";
import CollectionDelete from "@/components/actions/collection/CollectionDelete";

export default {
  name: "Collection",
  props: {
    collection: Object,
  },

  components: {
    CollectionUpdate,
    CollectionDelete,
  },
};
</script>

<style lang="scss" scoped>
.collection {
  text-align: left;

  .controls {
    display: flex;
    justify-content: space-between;
    padding-top: 12px;
    margin: 12px 0;
    border-top: 1px solid lightgray;
  }
}
</style>