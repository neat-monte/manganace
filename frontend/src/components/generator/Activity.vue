<template>
  <section id="activity">
    <swiper
      :preload-images="false"
      :lazy="true"
      :free-mode="true"
      :space-between="0"
      watch-slides-visibility
      navigation
    >
      <swiper-slide v-for="(image, index) in generatedImages" :key="image.id">
        <div class="image-wrapper">
          <a-tooltip title="Try delete">
            <span class="delete-image" @click="destroyImage(image)">
              <close-outlined />
            </span>
          </a-tooltip>
          <img
            v-if="index <= preloadCount"
            @click="swapImage(index)"
            :src="image.url"
            class="swiper-lazy"
          />
          <img
            v-else
            @click="swapImage(index)"
            :data-src="image.url"
            class="swiper-lazy"
          />
        </div>
        <div v-if="index > preloadCount" class="swiper-lazy-preloader"></div>
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import { ref, watchEffect } from "vue";

import { CloseOutlined } from "@ant-design/icons-vue";
import SwiperCore, { Navigation, Lazy } from "swiper";
import { Swiper, SwiperSlide } from "swiper/vue";

import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";
import "swiper/components/navigation/navigation.scss";

SwiperCore.use([Navigation, Lazy]);

import useGenerator from "@/modules/generator";
import useGeneratorSessionImages from "@/modules/generatorSessionImages";

export default {
  name: "Activity",

  props: {
    preloadCount: {
      type: Number,
      default: 6,
    },
  },

  async setup() {
    const { currentSession, swapImage } = useGenerator();
    const {
      imagesBySessionId,
      loadImagesOfSessionAsync,
      tryDeleteImageAsync,
    } = useGeneratorSessionImages();

    const generatedImages = ref([]);

    watchEffect(() => {
      if (currentSession.id) {
        generatedImages.value = imagesBySessionId[currentSession.id];
      }
    });

    await loadImagesOfSessionAsync(currentSession.id);

    async function destroyImage(image) {
      await tryDeleteImageAsync(currentSession.id, image);
    }

    return {
      swapImage,
      generatedImages,
      destroyImage,
    };
  },

  components: {
    Swiper,
    SwiperSlide,
    CloseOutlined,
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
      height: 100%;
      width: 200px !important;
      cursor: pointer;

      .image-wrapper {
        position: relative;
        overflow: hidden;

        .delete-image {
          position: absolute;
          top: 0;
          right: 0;
          visibility: hidden;
          color: $danger;
          padding: 3px;
        }

        img {
          width: auto;
          height: 200px;
          border-radius: 2px;
          transition: all 0.2s ease-in-out;
        }
      }

      .swiper-lazy-preloader {
        width: 36px;
        height: 36px;
        border: 2px solid #fff;
        border-color: $primary transparent $primary transparent;
      }

      &:hover {
        .image-wrapper {
          .delete-image {
            z-index: 100;
            visibility: visible;
          }

          img {
            z-index: 99;
            box-shadow: $box-shadow-soft;
            transform: scale(1.05);
          }
        }
      }
    }
  }
}
</style>