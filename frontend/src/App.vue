<template>
  <div class="wrapper">
    <Header />
    <router-view />
    <Footer />
  </div>
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
/**
  This empty style tag is required
  to load the external CSS
*/
</style>
