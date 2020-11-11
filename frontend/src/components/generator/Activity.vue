<template>
  <section id="activity">
    <swiper
      :slides-per-view="6"
      :space-between="0"
      :lazy="true"
      navigation
      :pagination="{ clickable: true }"
      :scrollbar="{ draggable: true }"
    >
      <swiper-slide v-for="(image, index) in generatedImages" :key="index">
        <img @click="swapImage(index)" :src="image.url" />
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import useGenerator from "@/modules/generator";

import SwiperCore, { Navigation, Scrollbar } from "swiper";
import { Swiper, SwiperSlide } from "swiper/vue";

SwiperCore.use([Navigation, Scrollbar]);

export default {
  name: "Activity",

  async setup() {
    const { generatedImages, loadActivityAsync, swapImage } = useGenerator();

    await loadActivityAsync();

    return {
      swapImage,
      generatedImages,
    };
  },

  components: {
    Swiper,
    SwiperSlide,
  },
};

import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";
import "swiper/components/navigation/navigation.scss";
import "swiper/components/scrollbar/scrollbar.scss";
</script>

<style lang="scss" scoped>
#activity {
  max-width: 100%;

  .swiper-container {
    padding: 20px 0;
    border-radius: 2px;
    min-height: 110px;

    .swiper-slide {
      display: flex;
      cursor: pointer;

      img {
        width: 100%;
        height: auto;
        border-radius: 2px;
      }

      &:hover {
        z-index: 1;
      }
    }
  }
}

@include tablet {
  #activity {
    .swiper-container {
      box-shadow: $box-double-shadow;
    }
  }
}
</style>