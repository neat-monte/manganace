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
import ImageSave from "@/components/shared/modals/image/ImageSave";
import ImageDownload from "@/components/shared/modals/image/ImageDownload";
import ZoomableImage from "@/components/shared/image/ZoomableImage";
import Loading from "@/components/shared/display/Loading";

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