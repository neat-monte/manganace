<template>
  <section id="generated-image">
    <ZoomableImage
      :url="currentImage.url"
      :showLoading="isGenerating"
      :enableZoom="true"
    >
      <template v-slot:controls>
        <ImageDownload :imageUrl="currentImage.url" />
        <Suspense>
          <template #default>
            <ImageSave />
          </template>
          <template #fallback>
            <Loading />
          </template>
        </Suspense>
      </template>
    </ZoomableImage>
  </section>
</template>

<script>
import ImageSave from "@/components/actions/image/ImageSave";
import ImageDownload from "@/components/actions/image/ImageDownload";
import ZoomableImage from "@/components/shared/ZoomableImage";
import Loading from "@/components/shared/Loading";

import useGenerator from "@/modules/generator";

export default {
  name: "Image",

  setup() {
    const { currentImage, isGenerating } = useGenerator();

    return {
      currentImage,
      isGenerating,
    };
  },

  components: {
    ZoomableImage,
    ImageSave,
    ImageDownload,
    Loading,
  },
};
</script>


<style lang="scss" scoped>
#generated-image {
  padding: 20px;
}

@include tablet {
  #generated-image {
    padding: 0;
    border-radius: 2px;
    box-shadow: $box-double-shadow;
  }
}
</style>