<template>
  <header id="header">
    <router-link class="brand-link" to="/">
      <div class="brand">
        <span class="title">Manganace</span>
        <span class="subtitle">Manipulate GAN Face</span>
      </div>
    </router-link>
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
  padding: 20px 0;

  .brand-link {
    display: flex;
    align-items: center;
    justify-content: center;

    .brand {
      flex: 0;
      display: flex;
      flex-wrap: wrap;

      .title {
        flex: 100%;
        font-size: 2.4rem;
        font-weight: bold;
        text-transform: uppercase;
        color: $primary;
      }
      .subtitle {
        flex: 100%;
        margin-top: -18px;
        font-size: 1.2rem;
        color: $primary-dark;
        transition: all 0.2s ease;
      }

      &:hover {
        .subtitle {
          color: $darkness;
          transform: scale(1.3);
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
      justify-content: center;
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

      &:hover {
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
    padding-left: 30px;
    padding-right: 30px;
    display: flex;

    .brand-link {
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
    padding-left: $sm-y-padding;
    padding-right: $sm-y-padding;

    .brand-link {
      justify-content: left;

      .brand {
        flex: 0 300px;
      }
    }
  }
}

@include lg-desktop {
  #header {
    padding-left: $lg-y-padding;
    padding-right: $lg-y-padding;
  }
}
</style>