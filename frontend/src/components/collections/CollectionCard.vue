<template>
  <div class="collection-card">
    <div class="card-content-wrapper">
      <div class="image-wrapper">
        <img :src="repImage" :alt="repImageDesc" />
      </div>
      <div class="content">
        <h3>{{ collection.name }}</h3>
        <p>{{ collection.description }}</p>
      </div>
      <div class="stats">
        <span>Images: {{ collection.imagesIds.length }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import useLibrary from "@/modules/useLibrary";

export default {
  props: {
    collectionId: {
      type: Number,
    },
  },
  setup(props) {
    const { state } = useLibrary();

    const collection = state.collections[props.collectionId];

    let repImage = "./empty.png";
    let repImageDesc = "Place holder image for emply collection";

    if (collection.imagesIds) {
      repImage = state.images[collection.imagesIds[0]].filename;
      repImageDesc = state.images[collection.imagesIds[0]].description;
    }
    return {
      collection,
      repImage,
      repImageDesc,
    };
  },
};
</script>