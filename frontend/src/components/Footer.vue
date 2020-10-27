<template>
  <footer id="footer">
    <div class="copyright">
      {{ new Date().getFullYear() }} © Radboud University
    </div>
    <div class="radboud">
      <img src="/radboud.png" alt="Radboud University" />
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
  padding: 16px 20px;

  background: $primary;
  color: $filler;

  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;

  position: absolute;
  bottom: 0;

  .copyright {
    flex: 1 200px;
    text-align: left;
  }

  .radboud {
    flex: 1 200px;
    min-width: 200px;
    max-width: 300px;

    img {
      width: 100%;
      height: auto;
    }
  }
}
</style>