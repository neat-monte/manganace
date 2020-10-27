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
  flex-flow: column wrap;
  position: relative;
  min-height: 100vh;

  > .content {
    padding-bottom: $footer-height;
    min-height: 100vh;
    width: 100%;
  }
}

@include tablet {
  #app {
    #header {
      padding: 0 $tablet-x-padding;
    }

    > .content {
      padding: 10px $tablet-x-padding ($footer-height + 10px) $tablet-x-padding;
    }

    #footer {
      padding: 0 $tablet-x-padding;
    }
  }
}

@include sm-desktop {
  #app {
    #header {
      padding: 0 $sm-x-padding;
    }

    > .content {
      padding: 20px $sm-x-padding ($footer-height + 20px) $sm-x-padding;
    }

    #footer {
      padding: 0 $sm-x-padding;
    }
  }
}

@include lg-desktop {
  #app {
    #header {
      padding: 0 $lg-x-padding;
    }

    > .content {
      padding: 40px $lg-x-padding ($footer-height + 40px) $lg-x-padding;
    }

    #footer {
      padding: 0 $lg-x-padding;
    }
  }
}
</style>
