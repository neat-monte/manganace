<template>
  <section id="images">
    <div v-if="collection" class="title-and-meta">
      <span class="title">
        {{ collection.name }}
      </span>
      <span class="meta">{{ Object.keys(images).length }} images</span>
    </div>
    <ImagesList :images="images" />
    <Empty v-if="images.length == 0" />
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";

import ImagesList from "@/components/shared/ImagesList";
import Empty from "@/components/shared/Empty";

import useImages from "@/modules/images";
import useCollections from "@/modules/collections";

export default {
  name: "Images",

  props: {
    collectionId: Number,
  },

  async setup(props) {
    const { collectionsById, collectionsLoaded } = useCollections();
    const { imagesByCollectionId, loadImagesOfCollectionAsync } = useImages();
    const collection = ref(null);
    const images = ref([]);
    const filterTags = ref([]);

    watchEffect(async () => {
      if (
        props.collectionId &&
        props.collectionId in collectionsById &&
        collectionsLoaded
      ) {
        collection.value = collectionsById[props.collectionId];
        await loadImagesOfCollectionAsync(props.collectionId);

        if (imagesByCollectionId[props.collectionId]) {
          images.value = imagesByCollectionId[props.collectionId];
        }

        filterTags.value = [];
      }
    });

    return {
      filterTags,
      images,
      collection,
    };
  },

  components: {
    ImagesList,
    Empty,
  },
};
</script>

<style lang="scss" scoped>
#images {
  .title-and-meta {
    flex: 100%;
    display: flex;
    padding: 20px 0;
    align-items: center;
    margin-bottom: 10px;

    .title {
      flex: 1 70%;
      text-align: left;
      margin: 0;
    }

    .meta {
      flex: 1;
      font-style: italic;
      text-align: right;
    }
  }
}
</style>