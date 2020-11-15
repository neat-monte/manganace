<template>
  <section id="activity">
    <swiper
      :slides-per-view="slidesCount"
      :space-between="5"
      :preload-images="false"
      :lazy="true"
      watch-slides-visibility
      navigation
    >
      <swiper-slide v-for="(image, index) in generatedImages" :key="index">
        <img
          v-if="index < slidesCount"
          @click="swapImage(index)"
          :src="image.url"
        />
        <img
          v-else
          @click="swapImage(index)"
          :data-src="image.url"
          class="swiper-lazy"
        />
        <div v-if="slidesCount <= index" class="swiper-lazy-preloader"></div>
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";
import useGenerator from "@/modules/generator";
import useActivity from "@/modules/activity";

import SwiperCore, { Navigation, Lazy } from "swiper";
import { Swiper, SwiperSlide } from "swiper/vue";

import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";
import "swiper/components/navigation/navigation.scss";

SwiperCore.use([Navigation, Lazy]);

export default {
  name: "Activity",

  props: {
    slidesCount: {
      type: Number,
      default: 6,
    },
  },

  setup() {
    const { currentSession, swapImage } = useGenerator();
    const { imagesBySessionId, loadImagesOfSessionAsync } = useActivity();

    const generatedImages = ref([]);

    watchEffect(async () => {
      const sessionId = currentSession.id;
      if (sessionId !== undefined) {
        await loadImagesOfSessionAsync(currentSession.id);
        generatedImages.value = imagesBySessionId[currentSession.id];
      }
    });

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
</script>

<style lang="scss" scoped>
#activity {
  height: 186px;

  .swiper-container {
    width: 100%;
    height: 100%;
    background: $darkness-05;
    border-radius: 2px;

    .swiper-slide {
      text-align: center;
      cursor: pointer;

      img {
        width: 100%;
        height: auto;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        border-radius: 2px;
      }

      .swiper-lazy-preloader {
        width: 36px;
        height: 36px;
        border: 2px solid #fff;
        border-color: $primary transparent $primary transparent;
      }

      &:hover {
        z-index: 1;
      }
    }
  }
}
</style>