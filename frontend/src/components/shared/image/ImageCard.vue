<template>
  <div class="image-card">
    <a-tooltip v-lazyload placement="top" :title="image.description">
      <LazyImage :src="image.url" :alt="image.description" />
    </a-tooltip>
    <div class="card-controls">
      <ImageDelete v-if="allowDelete" :imageId="image.id" />
      <ImageUpdate v-if="allowUpdate" :image="image" />
      <ImageDownload v-if="allowDownload" :imageUrl="image.url" />
    </div>
  </div>
</template>

<script>
import ImageDelete from "@/components/shared/modals/image/ImageDelete";
import ImageUpdate from "@/components/shared/modals/image/ImageUpdate";
import ImageDownload from "@/components/shared/modals/image/ImageDownload";
import LazyImage from "@/components/shared/image/LazyImage";

export default {
  name: "ImageCard",

  props: {
    image: Object,
    allowDelete: {
      type: Boolean,
      default: false,
    },
    allowUpdate: {
      type: Boolean,
      default: false,
    },
    allowDownload: {
      type: Boolean,
      default: false,
    },
  },

  components: {
    ImageDelete,
    ImageUpdate,
    ImageDownload,
    LazyImage,
  },
};
</script>

<style lang="scss" scoped>
.image-card {
  min-height: 230px;
  position: relative;
  margin-bottom: 20px;
  box-shadow: $box-shadow-strong;

  .card-controls {
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

    .card-controls {
      border-bottom: none;
    }
  }
}

@include sm-desktop {
  .image-card {
    overflow: hidden;

    .card-controls {
      position: absolute;
      background: $filler-35;
      bottom: -40px;
      left: 0;
      transition: all 0.2s ease;
      height: 40px;
      visibility: hidden;
    }

    &:hover {
      .card-controls {
        bottom: 0;
        visibility: visible;
      }
    }
  }
}
</style>