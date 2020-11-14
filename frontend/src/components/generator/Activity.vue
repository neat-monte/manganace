<template>
  <section id="activity">
    <swiper
      :slides-per-view="6"
      :space-between="20"
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
import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";
import "swiper/components/navigation/navigation.scss";
import "swiper/components/scrollbar/scrollbar.scss";

import { ref, watchEffect } from "vue";
import useGenerator from "@/modules/generator";
import useActivity from "@/modules/activity";

import SwiperCore, { Navigation, Scrollbar } from "swiper";
import { Swiper, SwiperSlide } from "swiper/vue";

SwiperCore.use([Navigation, Scrollbar]);

export default {
  name: "Activity",

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
  .swiper-container {
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
</style>