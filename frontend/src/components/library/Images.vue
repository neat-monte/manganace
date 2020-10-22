<template>
  <div id="images">
    {{ collectionId }}
    <div v-for="image in images" :key="image.id">
      {{ image.filename }}
    </div>
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";
import useImages from "@/modules/useImages";

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
};
</script>