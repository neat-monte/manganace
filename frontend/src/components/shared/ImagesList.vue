<template>
  <div id="image-cards-list">
    <div class="image-filter">
      <Suspense>
        <template #default>
          <TagSelect
            @tag-id-set="filterImagesByTags"
            :initialTags="filterTags"
            :showCreate="false"
            placeholder="Filter by tags"
          />
        </template>
      </Suspense>
    </div>
    <div class="images-list">
      <Suspense v-for="image in internalImages" :key="image.id">
        <template #default>
          <ImageCardAsync
            :image="image"
            :allowDelete="allowDelete"
            :allowUpdate="allowUpdate"
            :allowDownload="allowDownload"
          />
        </template>
        <template #fallback>
          <Loading id="image-card" />
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
      default: true,
    },
    allowUpdate: {
      type: Boolean,
      default: true,
    },
    allowDownload: {
      type: Boolean,
      default: true,
    },
  },

  setup(props) {
    const internalImages = ref([]);

    watchEffect(() => {
      internalImages.value = props.images;
    });

    function includesAll(array, values) {
      for (var i = 0; i < values.length; i++) {
        if (!array.includes(values[i])) {
          return false;
        }
      }
      return true;
    }

    function filterImagesByTags(tags) {
      if (tags.length > 0) {
        internalImages.value = Object.assign(
          {},
          Object.values(internalImages.value).filter((image) =>
            includesAll(image.tagsIds, tags)
          )
        );
      } else if (props.images) {
        internalImages.value = props.images;
      }
    }

    return {
      filterImagesByTags,
      internalImages,
    };
  },

  components: {
    Loading,
    TagSelect,
    ImageCardAsync: defineAsyncComponent({
      loader: () => import("@/components/shared/ImageCard"),
      delay: 200,
      suspensible: true,
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