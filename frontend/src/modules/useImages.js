import { reactive, readonly } from 'vue'
import http from '@/services/http'

const state = reactive({
  images: {}
})

export default function useImages() {
  const getImagesOfCollection = async (collectionId) => {
    if (collectionId in state.images)
      return;

    const images = await http.images.getImagesOfCollecton(collectionId);

    let imgDict = {}
    images.forEach(image => {
      imgDict[image.id] = image;
    });
    state.images[collectionId] = imgDict;
  }

  return {
    state: readonly(state),
    getImagesOfCollection
  }
}