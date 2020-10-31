<template>
  <header id="header">
    <div class="brand">
      <router-link class="brand-link" to="/">
        <span class="title">Manganace</span>
        <span class="subtitle">Manipulate GAN Face</span>
      </router-link>
    </div>
    <nav class="navigation">
      <router-link to="/">
        <div class="link">
          <PictureOutlined />
          <span>Library</span>
        </div>
      </router-link>
      <router-link to="/generator">
        <div class="link">
          <InteractionOutlined />
          <span>Generator</span>
        </div>
      </router-link>
    </nav>
  </header>
</template>

<script>
import { PictureOutlined, InteractionOutlined } from "@ant-design/icons-vue";

export default {
  name: "Header",

  components: {
    PictureOutlined,
    InteractionOutlined,
  },
};
</script>

<style lang="scss" scoped>
#header {
  height: $header-height;
  padding: 20px initial;

  .brand {
    display: flex;
    align-items: center;
    justify-content: center;

    .brand-link {
      flex: 0;
      display: flex;
      flex-wrap: wrap;

      .title {
        flex: 100%;
        font-size: 2.4rem;
        font-weight: bold;
        text-transform: uppercase;
        color: $primary;
        text-shadow: $text-shadow-hard;
        transition: all 0.2s ease;
      }

      .subtitle {
        flex: 100%;
        margin-top: -18px;
        font-size: 1.2rem;
        color: $primary-dark;
        text-shadow: $text-shadow-soft;
        transition: all 0.2s ease;
      }

      &:hover,
      &:focus {
        box-shadow: none !important;

        .title {
          text-shadow: $text-shadow-soft;
        }

        .subtitle {
          color: $darkness;
          text-shadow: $text-shadow-hard;
          transform: scale(1.2);
        }
      }
    }
  }

  .navigation {
    display: none;

    a {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: right;
      transition: all 0.2s ease;

      .link {
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;

        &::after {
          content: " ";
          height: 4px;
          width: 100%;
          background: $primary-dark;
          position: absolute;
          bottom: -10px;
          visibility: hidden;
          transform: scaleX(0);
          transition: all 0.3s ease-in-out 0s;
        }

        .anticon {
          margin-right: 10px;
          font-size: 1.8rem;
          color: $secondary;
        }

        span {
          font-size: 1rem;
          font-weight: bold;
          text-transform: uppercase;
          color: $primary;
        }
      }

      &:hover,
      &:focus {
        box-shadow: none !important;

        .link::after {
          visibility: visible;
          transform: scaleX(1);
        }
      }
    }
  }
}

@include tablet {
  #header {
    display: flex;

    .brand {
      flex: 3 400px;
    }

    .navigation {
      flex: 3;
      display: flex;

      > * {
        margin-right: 40px;
      }

      :last-child {
        margin: 0;
      }
    }
  }
}

@include sm-desktop {
  #header {
    .brand {
      justify-content: left;

      .brand-link {
        margin-left: 62px;
      }
    }
  }
}
</style>