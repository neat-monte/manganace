import { reactive, readonly } from 'vue'
import endpoints from "@/services/http/endpoints"
import http from '@/services/http'

const state = reactive({
  collectionImages: {},
})

function insertImage(image) {
  image.path = `${endpoints.baseAddress}${endpoints.static}/${image.filename}`;
  if (state.collectionImages[image.collectionId] === undefined) {
    state.collectionImages[image.collectionId] = {};
  }
  state.collectionImages[image.collectionId][image.id] = image;
}

export default function useImages() {
  const loadImagesOfCollection = async (collectionId) => {
    if (collectionId in state.collectionImages)
      return;
    const images = await http.images.getImagesOfCollecton(collectionId);
    images.forEach(image => insertImage(image));
  }

  const updateImage = async (updatedImage) => {
    const imageJson = JSON.stringify(updatedImage);
    const image = await http.images.update(updatedImage.id, imageJson)
    if (image) {
      insertImage(image);
      return state.collectionImages[image.collectionId][image.id];
    }
  }

  const deleteImage = async (imageId) => {
    const image = await http.images.destroy(imageId);
    if (image) {
      const deleted = state.collectionImages[image.collectionId][image.id]
      delete state.collectionImages[image.collectionId][image.id];
      return deleted;
    }
  }

  return {
    state: readonly(state),
    loadImagesOfCollection,
    updateImage,
    deleteImage
  }
}