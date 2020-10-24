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

<style lang="scss" scoped>
@include sm-desktop {
  .image-card {
    // height: 100px;
    // width: 100px;

    .card-content {
      .image-wrapper {
        img {
          object-fit: cover;
          height: 100%;
          width: 100%;
          right: 0;
        }
      }

      .content {
      }
    }
  }
}
</style>