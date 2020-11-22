<template>
  <header id="header">
    <div class="brand">
      <router-link class="brand-link" to="/">
        <span class="title">Manganace</span>
        <span class="subtitle">Manipulate GAN Face</span>
      </router-link>
    </div>
    <nav class="navigation">
      <router-link :to="{ name: 'Collections' }">
        <div class="link">
          <picture-outlined />
          <span>Library</span>
        </div>
      </router-link>
      <router-link :to="{ name: 'Generator' }">
        <div class="link">
          <interaction-outlined />
          <span>Generator</span>
        </div>
      </router-link>
      <router-link :to="{ name: 'Research' }">
        <div class="link">
          <experiment-outlined />
          <span>Research</span>
        </div>
      </router-link>
    </nav>
  </header>
</template>

<script>
import {
  PictureOutlined,
  InteractionOutlined,
  ExperimentOutlined,
} from "@ant-design/icons-vue";

export default {
  name: "Header",

  components: {
    PictureOutlined,
    InteractionOutlined,
    ExperimentOutlined,
  },
};
</script>

<style lang="scss" scoped>
#header {
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
        text-shadow: $text-shadow-soft;
        transition: all 0.2s ease;
      }

      .subtitle {
        flex: 100%;
        margin-top: -28px;
        font-size: 1.2rem;
        color: $primary-dark;
        transition: all 0.2s ease;
      }

      &:hover,
      &:focus {
        box-shadow: none !important;

        .subtitle {
          color: $darkness-80;
          transform: scale(1.1);
        }
      }
    }
  }

  .navigation {
    flex: 100%;
    display: flex;

    a {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      margin: 20px 0;

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
          display: block;
          font-size: 1.8rem;
          color: $secondary;
        }

        span {
          display: none;
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
    height: $header-height;
    display: flex;

    .brand {
      flex: 3 400px;
    }

    .navigation {
      flex: 3;
      display: flex;

      a {
        justify-content: right;
        margin-right: 10px;

        .link {
          .anticon {
            margin-right: 10px;
          }

          span {
            display: block;
          }
        }
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

    .navigation {
      a {
        margin-right: 40px;
      }

      :last-child {
        margin: 0;
      }
    }
  }
}
</style>