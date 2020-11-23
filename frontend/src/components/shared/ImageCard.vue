<template>
  <a-tooltip placement="top" :title="image.description">
    <div class="image-card">
      <div class="image-wrapper">
        <img :src="image.url" />
      </div>
      <div class="info">
        <div class="tags"></div>
      </div>
      <div class="card-controls">
        <ImageDelete v-if="allowDelete" :imageId="image.id" />
        <ImageDownload v-if="allowDownload" :imageUrl="image.url" />
        <ImageUpdate v-if="allowUpdate" :image="image" />
      </div>
    </div>
  </a-tooltip>
</template>

<script>
import ImageDelete from "@/components/actions/image/ImageDelete";
import ImageUpdate from "@/components/actions/image/ImageUpdate";
import ImageDownload from "@/components/actions/image/ImageDownload";

import lazyLoadImageCard from "@/directives/lazyLoadImageCard";

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

  directives: {
    lazyload: lazyLoadImageCard,
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
  min-height: 40px;
  position: relative;
  margin-bottom: 20px;
  box-shadow: $box-shadow-strong;

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

    .image-wrapper img {
      border-radius: 2px 2px 0 0;
    }

    .card-controls {
      border-bottom: none;
    }
  }
}

@include sm-desktop {
  .image-card {
    overflow: hidden;

    .info {
      position: absolute;
      top: 0;
      left: 0;
      visibility: hidden;
      display: none;
    }

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