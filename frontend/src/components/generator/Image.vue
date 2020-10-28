<template>
  <section id="generated-image">
    <div class="controls">
      <button>Add</button>
      <ImageDownload :imageUrl="image.path" />
    </div>
    <div class="image-wrapper">
      <Loading v-if="isGenerating" />
      <img :src="image.path" />
      <div
        class="zoomed-in"
        :style="`background-image: url('${image.path}')`"
        @mousemove="ZoomIn"
      />
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

    function ZoomIn(event) {
      var genImage = document.getElementById("generated-image"),
        imageWrapper = genImage.getElementsByClassName("image-wrapper")[0];

      var position = {
        x: Math.round(
          (event.clientX - (imageWrapper.offsetLeft - window.scrollX)) /
            (event.target.offsetWidth / 100)
        ),
        y: Math.round(
          (event.clientY - (imageWrapper.offsetTop - window.scrollY)) /
            (event.target.offsetHeight / 100)
        ),
      };

      event.target.style.backgroundPosition =
        position.x + "% " + position.y + "%";
    }

    return {
      image,
      isGenerating,
      ZoomIn,
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
    position: relative;
    height: 100vw;
    overflow: hidden;

    img {
      object-fit: cover;
      width: 100%;
      height: auto;
      border-radius: 2px;
    }

    .zoomed-in {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      opacity: 0;
      transition: opacity 0.2s linear;
    }

    .loading {
      position: absolute;
      background: $secondary-50;
      height: 100%;
    }

    &:hover {
      .zoomed-in {
        opacity: 1;
      }
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
      padding: 20px 0;
    }

    .image-wrapper {
      width: 512px;
      height: 512px;
    }
  }
}
</style>