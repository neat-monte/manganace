<template>
  <div id="zoomable-image">
    <div id="zoomable-image-wrapper">
      <Loading v-if="showLoading" />
      <img :src="url" />
      <div
        v-if="enableZoom"
        class="zoomed-in"
        :style="`background-image: url('${url}')`"
        @mousemove="ZoomIn"
      />
    </div>
    <div class="controls">
      <slot name="controls"></slot>
    </div>
  </div>
</template>

<script>
import Loading from "@/components/shared/Loading";

export default {
  name: "ZoomableImage",

  props: {
    url: {
      type: String,
    },
    showLoading: {
      type: Boolean,
      default: false,
    },
    enableZoom: {
      type: Boolean,
      default: false,
    },
  },

  setup() {
    function ZoomIn(event) {
      const wrapper = document.getElementById("zoomable-image");

      const position = {
        x: Math.round(
          (event.clientX - (wrapper.offsetLeft - window.scrollX)) /
            (event.target.offsetWidth / 100)
        ),
        y: Math.round(
          (event.clientY - (wrapper.offsetTop - window.scrollY)) /
            (event.target.offsetHeight / 100)
        ),
      };

      event.target.style.backgroundPosition =
        position.x + "% " + position.y + "%";
    }

    return {
      ZoomIn,
    };
  },

  components: {
    Loading,
  },
};
</script>

<style lang="scss" scoped>
#zoomable-image {
  margin: auto;

  #zoomable-image-wrapper {
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

  .controls {
    flex: 100%;
    padding: 20px;
    display: flex;
    justify-content: space-around;
  }
}

@include tablet {
  #zoomable-image {
    border-radius: 2px;
    box-shadow: $box-shadow-strong;
  }
}

@include sm-desktop {
  #zoomable-image {
    width: 512px;

    #zoomable-image-wrapper {
      height: 512px;
      width: 512px;
    }
  }
}
</style>