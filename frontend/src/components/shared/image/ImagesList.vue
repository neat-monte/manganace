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
        <template #fallback>
          <Loading />
        </template>
      </Suspense>
    </div>
    <div class="images-list">
      <ImageCard
        v-for="image in internalImages"
        :key="image.id"
        :image="image"
        :allowDelete="allowDelete"
        :allowUpdate="allowUpdate"
        :allowDownload="allowDownload"
      />
    </div>
    <Empty v-if="images.length == 0" />
  </div>
</template>

<script>
import { ref, watchEffect } from "vue";

import ImageCard from "@/components/shared/image/ImageCard";
import TagSelect from "@/components/shared/modals/tag/TagSelect";
import Loading from "@/components/shared/display/Loading";
import Empty from "@/components/shared/display/Empty";

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
    ImageCard,
    Empty,
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