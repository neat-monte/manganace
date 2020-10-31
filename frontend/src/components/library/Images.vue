<template>
  <section id="images">
    <div v-if="collection" class="upper-controls">
      <div class="title-and-meta">
        <span class="title">
          {{ collection.name }}
        </span>
        <span class="meta">{{ Object.keys(images).length }} images</span>
      </div>
    </div>
    <div class="images-list">
      <Suspense v-for="image in images" :key="image.id">
        <template #default>
          <ImageCardAsync :image="image" />
        </template>
        <template #fallback>
          <Loading id="image-card" />
        </template>
      </Suspense>
    </div>
  </section>
</template>

<script>
import { defineAsyncComponent, ref, watchEffect } from "vue";

import Loading from "@/components/shared/Loading";
import useImages from "@/modules/useImages";
import useCollections from "@/modules/useCollections";

export default {
  name: "Images",

  props: {
    collectionId: Number,
  },

  async setup(props) {
    const { imagesByCollection, loadImagesOfCollection } = useImages();
    const { collectionsLoaded, collectionsById } = useCollections();
    const collection = ref(null);
    const images = ref([]);

    watchEffect(async () => {
      if (props.collectionId && collectionsLoaded) {
        collection.value = collectionsById[props.collectionId];
        await loadImagesOfCollection(props.collectionId);
        images.value = imagesByCollection[props.collectionId];
      }
    });

    return {
      images,
      collection,
    };
  },

  components: {
    Loading,
    ImageCardAsync: defineAsyncComponent({
      loader: () => import("@/components/library/ImageCard"),
      // loadingComponent: Loading,
      delay: 200,
      suspensible: true,
    }),
  },
};
</script>

<style lang="scss" scoped>
#images {
  .upper-controls {
    min-height: 50px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    padding: 20px;

    .title-and-meta {
      flex: 100%;
      display: flex;
      align-items: center;

      .title {
        flex: 1 70%;
        text-align: left;
      }

      .meta {
        flex: 1;
        font-style: italic;
        text-align: right;
      }
    }
  }
}

@include tablet {
  #images {
    .upper-controls {
      margin-bottom: 20px;
      box-shadow: $box-double-shadow;
    }

    .images-list {
      display: grid;
      grid-gap: 10px;
      grid-template-columns: repeat(3, 1fr);
    }
  }
}

@include sm-desktop {
  #images {
    margin-left: 50px;

    .images-list {
      grid-gap: 20px;
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
</style>