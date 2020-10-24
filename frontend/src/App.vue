<template>
  <Header />
  <router-view />
  <Footer />
</template>

<script>
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style lang="scss">
#app {
  background: $filler;
  display: flex;
  flex-direction: column;
  position: relative;
  min-height: 100vh;

  > .content {
    padding-bottom: $footer-height;
  }
}

@include sm-desktop {
  #app > .content {
    padding: 20px $sm-y-padding $footer-height $sm-y-padding;
  }
}

@include lg-desktop {
  #app > .content {
    padding: 40px $lg-y-padding $footer-height $lg-y-padding;
  }
}
</style>
