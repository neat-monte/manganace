<template>
  <section id="generated-image">
    <div class="controls">
      <button>Add</button>
      <ImageDownload />
    </div>
    <div class="image-wrapper">
      <Loading v-if="isGenerating" />
      <img :src="image.path" />
    </div>
  </section>
</template>


<script>
import useGenerator from "@/modules/useGenerator";
import ImageDownload from "@/components/library/images/ImageDownload";
import Loading from "@/components/shared/Loading";

export default {
  name: "Image",

  setup() {
    const { image, isGenerating } = useGenerator();

    return {
      image,
      isGenerating,
    };
  },

  components: {
    Loading,
    ImageDownload,
  },
};
</script>


<style lang="scss" scoped>
#generated-image {
  .controls {
    text-align: right;
    padding: 20px 50px;
  }

  .image-wrapper {
    background: $secondary-20;
    position: relative;
    height: 100vw;

    img {
      object-fit: cover;
      width: 100%;
      height: auto;
      border-radius: 2px;
    }

    .loading {
      position: absolute;
      background: $secondary-50;
      height: 100%;
    }
  }
}

@include tablet {
  // viewport width minus padding from both sides:
  $height: calc(100vw - (#{$tablet-x-padding} * 2));

  #generated-image {
    .image-wrapper {
      height: $height;
      border-radius: 2px;
      box-shadow: $box-double-shadow;
    }
  }
}

@include sm-desktop {
  #generated-image {
    display: flex;
    flex-flow: row wrap;
    justify-content: right;

    .controls {
      flex: 1 100%;
    }

    .image-wrapper {
      width: 512px;
      height: 512px;
    }
  }
}
</style>