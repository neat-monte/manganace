<template>
  <div v-lazyload class="image-wrapper">
    <img :data-url="src" :alt="alt" />
    <Loading class="loader" />
  </div>
</template>

<script>
import LazyLoadImageDirective from "@/directives/LazyLoadImageDirective";
import Loading from "@/components/shared/Loading";

export default {
  inheritAttrs: false,

  props: {
    src: {
      type: String,
      required: true,
    },
    alt: String,
  },

  directives: {
    lazyload: LazyLoadImageDirective,
  },

  components: {
    Loading,
  },
};
</script>

<style lang="scss" scoped>
.image-wrapper {
  display: block;
  width: 100%;
  height: 100%;

  img {
    object-fit: cover;
    width: 100%;
    height: auto;
    opacity: 0;
    transition: opacity 300ms ease;
  }

  &.loaded {
    img {
      opacity: 1;
    }

    .loader {
      display: none;
    }
  }
}
</style>