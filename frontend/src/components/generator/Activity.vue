<template>
  <section id="activity">
    <swiper
      :preload-images="false"
      :lazy="true"
      :free-mode="true"
      :breakpoints="{
        320: {
          slidesPerView: 1,
          spaceBetween: 10,
        },
        480: {
          slidesPerView: 2,
          spaceBetween: 10,
        },
        768: {
          slidesPerView: 3,
          spaceBetween: 10,
        },
        992: {
          slidesPerView: 4,
          spaceBetween: 10,
        },
        1200: {
          slidesPerView: 5,
          spaceBetween: 10,
        },
        1400: {
          slidesPerView: maxSlidesCount,
        },
      }"
      watch-slides-visibility
      navigation
    >
      <swiper-slide v-for="(image, index) in generatedImages" :key="index">
        <img
          v-if="index < maxSlidesCount"
          @click="swapImage(index)"
          :src="image.url"
        />
        <img
          v-else
          @click="swapImage(index)"
          :data-src="image.url"
          class="swiper-lazy"
        />
        <div v-if="maxSlidesCount <= index" class="swiper-lazy-preloader"></div>
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
    maxSlidesCount: {
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
  height: 220px;
  border-radius: 2px;
  border: 1px solid $darkness-20;

  .swiper-container {
    height: 100%;
    background: $darkness-05;

    .swiper-slide {
      display: flex;
      justify-content: center;
      align-items: center;
      cursor: pointer;

      img {
        width: auto;
        height: 200px;
        border-radius: 2px;
      }

      .swiper-lazy-preloader {
        width: 36px;
        height: 36px;
        border: 2px solid #fff;
        border-color: $primary transparent $primary transparent;
      }

      &:hover {
        img {
          z-index: 1;
          box-shadow: $box-shadow-soft;
          transform: scale(1.04);
        }
      }
    }
  }
}
</style>