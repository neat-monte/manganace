<template>
  <div class="image-card">
    <div class="image-wrapper">
      <img :src="image.path" :alt="image.description" />
    </div>
    <div class="info">
      <p>{{ image.description }}</p>
      <div class="tags"></div>
    </div>
    <div class="controls">
      <ImageDelete :imageId="image.id" />
      <ImageDownload :imageUrl="image.path" />
      <ImageUpdate :image="image" />
    </div>
  </div>
</template>

<script>
import ImageDelete from "@/components/actions/image/ImageDelete";
import ImageUpdate from "@/components/actions/image/ImageUpdate";
import ImageDownload from "@/components/actions/image/ImageDownload";
// import useTags from "@/modules/useTags";

export default {
  name: "ImageCard",
  props: {
    image: Object,
  },

  components: {
    ImageDelete,
    ImageUpdate,
    ImageDownload,
  },
};
</script>

<style lang="scss" scoped>
.image-card {
  position: relative;
  margin-bottom: 20px;
  box-shadow: $box-double-shadow;

  .image-wrapper {
    display: block;
    width: 100%;

    img {
      object-fit: cover;
      width: 100%;
      height: auto;
    }
  }
  .info {
    padding-bottom: 50px;

    p {
      margin: 0;
    }
  }

  .controls {
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: absolute;
    bottom: 0;
    height: 50px;
    border-top: 1px solid $secondary-20;
  }
}

@include tablet {
  .image-card {
    margin: 0;
    border-radius: 2px 2px 2px 2px;

    .image-wrapper img {
      border-radius: 2px 2px 0 0;
    }

    .controls {
      border-bottom: none;
    }
  }
}
</style>