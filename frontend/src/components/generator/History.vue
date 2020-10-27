<template>
  <section id="history">
    <span class="title">History</span>
    <swiper :slides-per-view="8" :space-between="10">
      <swiper-slide v-for="item in history" :key="item">
        <img @click="clicked" :src="item.path" />
      </swiper-slide>
    </swiper>
  </section>
</template>

<script>
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/swiper.scss";
// import "swiper/components/navigation/navigation.scss";
// import "swiper/components/pagination/pagination.scss";
// import "swiper/components/scrollbar/scrollbar.scss";
import useGenerator from "@/modules/useGenerator";

export default {
  name: "History",

  setup() {
    const { state } = useGenerator();

    function clicked() {
      alert("clicked");
    }

    return {
      clicked,
      history: state.history,
    };
  },

  components: {
    Swiper,
    SwiperSlide,
  },
};
</script>

<style lang="scss" scoped>
#history {
  min-height: 200px;
  max-width: 100%;

  .swiper-container {
    width: 100%;

    .swiper-slide {
      display: flex;
      justify-content: center;
      align-items: center;

      // img {
      //   width: 128px;
      //   height: 128px;
      // }
    }
  }
}

@include sm-desktop {
  #history {
    margin-top: 10px;
  }
}

@include lg-desktop {
  #history {
    margin-top: 20px;
  }
}
</style>