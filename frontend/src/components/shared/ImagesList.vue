<template>
  <div id="image-cards-list">
    <div class="image-filter">
      <Suspense>
        <template #default>
          <TagSelect
            v-model="filterTags"
            :showCreate="false"
            placeholder="Filter by tags"
          />
        </template>
      </Suspense>
    </div>
    <div class="images-list">
      <Suspense v-for="image in internalImages" :key="image.id">
        <template #default>
          <ImageCard
            :image="image"
            :allowDelete="allowDelete"
            :allowUpdate="allowUpdate"
            :allowDownload="allowDownload"
          />
        </template>
        <template #fallback>
          <Loading />
        </template>
      </Suspense>
    </div>
  </div>
</template>

<script>
import { ref, defineAsyncComponent, watchEffect } from "vue";

import TagSelect from "@/components/actions/tag/TagSelect";
import Loading from "@/components/shared/Loading";

export default {
  name: "ImagesList",

  props: {
    images: [Object],
    allowDelete: {
      type: Boolean,
      default: false,
    },
    allowUpdate: {
      type: Boolean,
      default: false,
    },
    allowDownload: {
      type: Boolean,
      default: false,
    },
  },

  setup(props) {
    const internalImages = ref([]);
    const filterTags = ref([]);

    function includesAll(array, values) {
      for (var i = 0; i < values.length; i++) {
        if (!array.includes(values[i])) {
          return false;
        }
      }
      return true;
    }

    function filterImagesByTags() {
      if (filterTags.value.length > 0) {
        internalImages.value = Object.assign(
          {},
          Object.values(internalImages.value).filter((image) =>
            includesAll(image.tagsIds, filterTags.value)
          )
        );
      } else if (props.images) {
        internalImages.value = props.images;
      }
    }

    watchEffect(() => {
      internalImages.value = props.images;
      filterImagesByTags();
    });

    return {
      filterTags,
      internalImages,
    };
  },

  components: {
    Loading,
    TagSelect,
    ImageCard: defineAsyncComponent({
      loader: () => import("@/components/shared/ImageCard"),
      delay: 200,
      timeout: 3000,
      suspensible: false,
    }),
  },
};
</script>

<style lang="scss" scoped>
#image-cards-list {
  .image-filter {
    margin-bottom: 20px;
  }
}

@include tablet {
  #image-cards-list {
    .images-list {
      display: grid;
      grid-gap: 10px;
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
@include sm-desktop {
  #image-cards-list {
    .images-list {
      grid-gap: 20px;
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
</style>