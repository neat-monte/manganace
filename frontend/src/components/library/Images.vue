<template>
  <div class="images">
    <ImageCard v-for="image in images" :key="image.id" :image="image" />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";
import useImages from "@/modules/useImages";
import ImageCard from "@/components/library/ImageCard";

export default {
  name: "Images",

  props: {
    collectionId: Number,
  },

  async setup(props) {
    const { state, getImagesOfCollection } = useImages();
    const images = ref();

    watchEffect(async () => {
      await getImagesOfCollection(props.collectionId);
      images.value = state.images[props.collectionId];
    });

    return {
      images,
    };
  },

  components: {
    ImageCard,
  },
};
</script>

<style lang="scss" scoped>
@include sm-desktop {
  .images {
    padding: 10px 5%;
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(3, auto);
  }
}
</style>