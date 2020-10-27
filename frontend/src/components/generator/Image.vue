<template>
  <section id="generated-image">
    <div class="controls">
      <button>Add</button>
      <ImageDownload />
    </div>
    <div class="image-wrapper">
      <Loading v-if="generating" />
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
    const { state, generating } = useGenerator();

    return {
      image: state.image,
      generating,
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
    height: 40px;
  }

  .image-wrapper {
    background: $secondary-20;
    position: relative;

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
</style>