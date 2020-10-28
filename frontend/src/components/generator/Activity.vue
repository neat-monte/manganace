<template>
  <section id="activity">
    <swiper :slides-per-view="6" :space-between="0" :lazy="true">
      <swiper-slide v-for="(image, index) in images" :key="index">
        <img @click="swapImage(index)" :src="image.path" />
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";

import { Swiper, SwiperSlide } from "swiper/vue";

import useGenerator from "@/modules/useGenerator";

export default {
  name: "Activity",

  async setup() {
    const { activity, loadActivity, swapImage } = useGenerator();

    await loadActivity();

    return {
      swapImage,
      images: activity.images,
    };
  },

  components: {
    Swiper,
    SwiperSlide,
  },
};
</script>

<style lang="scss" scoped>
#activity {
  max-width: 100%;

  .swiper-container {
    padding: 20px 0;
    border-radius: 2px;

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