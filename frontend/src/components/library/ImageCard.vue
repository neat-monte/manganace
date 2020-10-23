<template>
  <div class="image-card">
    <div class="card-content">
      <div class="image-wrapper">
        <img :src="image.path" :alt="image.description" />
      </div>
      <!-- <p>{{ image.description }}</p> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "ImageCard",
  props: {
    image: Object,
  },
};
</script>