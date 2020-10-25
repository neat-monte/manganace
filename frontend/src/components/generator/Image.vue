<template>
  <section id="generated-image">
    <div class="image-wrapper">
      <img class="face" :src="image.path" />
    </div>
  </section>
</template>


<script>
import useGenerator from "@/modules/useGenerator";

export default {
  name: "Image",

  setup() {
    const { state } = useGenerator();

    return {
      image: state.image,
    };
  },
};
</script>


<style lang="scss" scoped>
#generated-image {
  flex: 1 100%;
  background: $secondary-20;

  .image-wrapper {
    position: relative;
    height: 100vw;
    width: 100%;

    .face {
      object-fit: cover;
      position: absolute;
      height: 100%;
      width: 100%;
      right: 0;
    }
  }
}

$image-dims: calc(100vw * 0.6);

@include tablet {
  #generated-image {
    flex: 0 $image-dims;
    max-height: $image-dims;

    .image-wrapper {
      height: $image-dims;
      width: 100%;
    }
  }
}

$image-dims: calc((100vw - 2 * #{$sm-y-padding}) * 0.5);

@include sm-desktop {
  #generated-image {
    flex: 0 $image-dims;
    max-height: $image-dims;

    .image-wrapper {
      height: $image-dims;
    }
  }
}

$image-dims: calc((100vw - 2 * #{$lg-y-padding}) * 0.5);

@include lg-desktop {
  #generated-image {
    flex: 0 $image-dims;
    max-height: $image-dims;
    max-width: $lg-desktop-image;

    .image-wrapper {
      height: $image-dims;
      max-height: $lg-desktop-image;
      max-width: $lg-desktop-image;
    }
  }
}
</style>