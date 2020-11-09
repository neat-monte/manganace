import { reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"

const loaded = reactive({});
const imagesByCollectionId = reactive({});

function insertImage(image) {
  if (imagesByCollectionId[image.collectionId] === undefined) {
    imagesByCollectionId[image.collectionId] = {};
  }
  imagesByCollectionId[image.collectionId][image.id] = image;
}

export default function useImages() {

  const loadImagesOfCollection = async (collectionId) => {
    if (loaded !== undefined && collectionId in loaded && loaded[collectionId])
      return;
    try {
      const images = await api.images.getImagesOfCollecton(collectionId);
      images.forEach(image => insertImage(image));
      loaded[collectionId] = true;
    } catch {
      notification.images.failedToLoad();
    }
  }

  const createImage = async (newImage) => {
    try {
      const imageJson = JSON.stringify(newImage);
      const image = await api.images.create(imageJson);
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
      const image = await api.images.update(updatedImage.id, imageJson)
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
      const image = await api.images.destroy(imageId);
      if (image) {
        delete imagesByCollectionId[image.collectionId][imageId];
        notification.images.deleted(image);
      }
    } catch {
      notification.images.failedToDelete();
    }
  }

  return {
    imagesByCollectionId: readonly(imagesByCollectionId),
    loadImagesOfCollection,
    createImage,
    updateImage,
    deleteImage
  }
}