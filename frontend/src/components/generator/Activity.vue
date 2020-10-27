<template>
  <section id="activity">
    <swiper :slides-per-view="6" :space-between="5" :lazy="true">
      <swiper-slide v-for="(item, index) in activity" :key="index">
        <img @click="swapImage(index)" :src="item.path" />
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/swiper.scss";
import "swiper/components/lazy/lazy.scss";
import useGenerator from "@/modules/useGenerator";

export default {
  name: "Activity",

  async setup() {
    const { activity, loadActivity, swapImage } = useGenerator();

    await loadActivity();

    return {
      swapImage,
      activity,
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
  background: $secondary-20;

  .swiper-container {
    min-height: 220px;
    padding: 20px 0;
    border-radius: 2px;

    .swiper-slide {
      display: flex;
      cursor: pointer;

      img {
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

@include sm-desktop {
  #activity {
    margin-top: 10px;
  }
}

@include lg-desktop {
  #activity {
    margin-top: 20px;
  }
}
</style>