<template>
  <section id="generated-image">
    <div class="wrapper">
      <div class="image-wrapper">
        <Loading v-if="isGenerating" />
        <img :src="currentImage.path" />
        <div
          class="zoomed-in"
          :style="`background-image: url('${currentImage.path}')`"
          @mousemove="ZoomIn"
        />
      </div>
      <div class="controls">
        <Suspense>
          <template #default>
            <ImageSave />
          </template>
          <template #fallback>
            <Loading />
          </template>
        </Suspense>
        <ImageDownload :imageUrl="currentImage.path" />
      </div>
    </div>
  </section>
</template>

<script>
import ImageSave from "@/components/actions/image/ImageSave";
import ImageDownload from "@/components/actions/image/ImageDownload";
import Loading from "@/components/shared/Loading";
import useGenerator from "@/modules/generator";

export default {
  name: "Image",

  setup() {
    const { currentImage, isGenerating } = useGenerator();

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
      currentImage,
      isGenerating,
      ZoomIn,
    };
  },

  components: {
    Loading,
    ImageSave,
    ImageDownload,
  },
};
</script>


<style lang="scss" scoped>
#generated-image {
  padding: 20px;
  height: 100vw;

  .wrapper {
    margin: auto;

    .controls {
      padding: 20px 0;
      display: flex;
      justify-content: space-around;
    }

    .image-wrapper {
      position: relative;
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
        height: 100%;
      }

      &:hover {
        .zoomed-in {
          opacity: 1;
          cursor: move;
        }
      }
    }
  }
}

@include tablet {
  #generated-image {
    height: calc(100vw - 2 * #{$tablet-x-padding});
    border-radius: 2px;
    box-shadow: $box-double-shadow;
    margin-bottom: 20px;
  }
}

@include sm-desktop {
  #generated-image {
    height: initial;
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