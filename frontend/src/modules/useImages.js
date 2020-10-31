import { reactive, readonly } from 'vue'
import http from '@/services/http'

const state = reactive({
  loaded: {},
  imagesByCollection: {},
})

function insertImage(image) {
  if (state.imagesByCollection[image.collectionId] === undefined) {
    state.imagesByCollection[image.collectionId] = {};
  }
  state.imagesByCollection[image.collectionId][image.id] = image;
}

export default function useImages() {
  const loadImagesOfCollection = async (collectionId) => {
    if (state !== undefined && collectionId in state.loaded && state.loaded[collectionId])
      return;
    const images = await http.images.getImagesOfCollecton(collectionId);
    images.forEach(image => insertImage(image));
    state.loaded[collectionId] = true;
  }

  const createImage = async (newImage) => {
    const imageJson = JSON.stringify(newImage);
    const image = await http.images.create(imageJson);
    if (image) {
      insertImage(image);
      return state.imagesByCollection[image.collectionId][image.id];
    }
  }

  const updateImage = async (updatedImage) => {
    const imageJson = JSON.stringify(updatedImage);
    const image = await http.images.update(updatedImage.id, imageJson)
    if (image) {
      insertImage(image);
      return state.imagesByCollection[image.collectionId][image.id];
    }
  }

  const deleteImage = async (imageId) => {
    const image = await http.images.destroy(imageId);
    if (image) {
      const deleted = state.imagesByCollection[image.collectionId][image.id]
      delete state.imagesByCollection[image.collectionId][image.id];
      return deleted;
    }
  }

  return {
    imagesByCollection: readonly(state.imagesByCollection),
    loadImagesOfCollection,
    createImage,
    updateImage,
    deleteImage
  }
}