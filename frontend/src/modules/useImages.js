import { reactive, readonly } from 'vue'
import http from '@/services/http'
import notification from "@/services/notification"

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
    try {
      const images = await http.images.getImagesOfCollecton(collectionId);
      images.forEach(image => insertImage(image));
      state.loaded[collectionId] = true;
    } catch {
      notification.images.failedToLoad();
    }
  }

  const createImage = async (newImage) => {
    try {
      const imageJson = JSON.stringify(newImage);
      const image = await http.images.create(imageJson);
      if (image) {
        insertImage(image);
        notification.images.added(image);
      }
    } catch {
      notification.images.failedToAdd();
    }
  }

  const updateImage = async (updatedImage) => {
    try {
      const imageJson = JSON.stringify(updatedImage);
      const image = await http.images.update(updatedImage.id, imageJson)
      if (image) {
        insertImage(image);
        notification.images.updated(image);
      }
    } catch {
      notification.images.failedToUpdate();
    }
  }

  const deleteImage = async (imageId) => {
    try {
      const image = await http.images.destroy(imageId);
      if (image) {
        delete state.imagesByCollection[image.collectionId][image.id];
        notification.images.deleted(image);
      }
    } catch {
      notification.collections.failedToDelete();
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