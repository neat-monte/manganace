<template>
  <Header v-if="showHeader" />
  <router-view />
  <Footer />
</template>

<script>
import { ref, watchEffect } from "vue";
import { useRoute } from "vue-router";

import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default {
  setup() {
    const route = useRoute();
    const showHeader = ref(true);

    watchEffect(() => {
      showHeader.value = route.name !== "ResearchSession";
    });

    return {
      showHeader,
      route,
    };
  },

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
  flex-flow: column wrap;
  position: relative;
  min-height: 100vh;

  > .content {
    padding-bottom: $footer-height;
    min-height: calc(100vh - #{$header-height});
    width: 100%;
  }
}

@include tablet {
  #app {
    #header,
    #footer,
    > .content {
      padding-left: $tablet-x-padding;
      padding-right: $tablet-x-padding;
    }

    > .content {
      padding-bottom: $footer-height + 10px;
    }
  }
}

@include sm-desktop {
  #app {
    #header,
    #footer,
    > .content {
      padding-left: $sm-x-padding;
      padding-right: $sm-x-padding;
    }

    > .content {
      padding-bottom: $footer-height + 20px;
    }
  }
}

@include lg-desktop {
  #app {
    #header,
    #footer,
    > .content {
      padding-left: $lg-x-padding;
      padding-right: $lg-x-padding;
    }

    > .content {
      padding-bottom: $footer-height + 40px;
    }
  }
}
</style>
