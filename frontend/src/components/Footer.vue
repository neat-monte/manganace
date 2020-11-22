<template>
  <footer id="footer">
    <div class="copyright">
      {{ new Date().getFullYear() }} © Radboud University
    </div>
    <div class="radboud">
      <img class="full" src="/radboud.png" alt="Radboud University" />
      <img class="logo" src="/radboud-logo.png" alt="Radboud University" />
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<style lang="scss" scoped>
#footer {
  width: 100%;
  height: $footer-height;
  padding: 0 20px;
  background: $primary;
  color: $filler;

  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;

  position: absolute;
  bottom: 0;

  .copyright {
    text-align: left;
  }

  .radboud {
    .full,
    .logo {
      img {
        width: 100%;
        height: 100%;
      }
    }

    .full {
      display: none;
      max-height: 60px;
    }

    .logo {
      min-width: 50px;
      max-width: 50px;
    }
  }
}

@include tablet {
  #footer {
    padding: 0;

    .radboud {
      .full {
        display: block;
      }

      .logo {
        display: none;
      }
    }
  }
}
</style>