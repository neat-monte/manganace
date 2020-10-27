<template>
  <section id="images">
    <div class="controls"></div>
    <div class="images-list">
      <Suspense v-for="image in images" :key="image.id">
        <ImageCardAsync :image="image" />
      </Suspense>
    </div>
  </section>
</template>

<script>
import { defineAsyncComponent, ref, watchEffect } from "vue";
import Loading from "@/components/shared/Loading";
import useImages from "@/modules/useImages";

export default {
  name: "Images",

  props: {
    collectionId: Number,
  },

  async setup(props) {
    const { state, loadImagesOfCollection } = useImages();
    const images = ref();

    watchEffect(async () => {
      await loadImagesOfCollection(props.collectionId);
      images.value = state.collectionImages[props.collectionId];
    });

    return {
      images,
    };
  },

  components: {
    ImageCardAsync: defineAsyncComponent({
      loader: () => import("@/components/library/images/ImageCard"),
      loadingComponent: Loading,
      delay: 100,
      suspensible: false,
    }),
  },
};
</script>

<style lang="scss" scoped>
@include tablet {
  #images {
    .controls {
      height: 70px;
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
    .images-list {
      margin-left: 50px;
      grid-gap: 20px;
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
</style>