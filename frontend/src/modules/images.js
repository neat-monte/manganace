import { reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const loaded = reactive({});
const hasLoaded = (collectionId) => loaded !== undefined && collectionId in loaded && loaded[collectionId]
const loadLock = new AwaitLock();

const imagesByCollectionId = reactive({});

const insertImage = (image) => {
    if (imagesByCollectionId[image.collectionId] === undefined) {
        imagesByCollectionId[image.collectionId] = {};
    }
    imagesByCollectionId[image.collectionId][image.id] = image;
}

export default function useImages() {

    const loadImagesOfCollectionAsync = async (collectionId) => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded(collectionId)) {
                return;
            }
            const images = await api.collections.getImagesOfCollecton(collectionId);
            images.forEach(image => insertImage(image));
            hasLoaded[collectionId] = true;
        } catch {
            notification.images.failedToLoad();
        } finally {
            loadLock.release();
        }
    }

    const addImageAsync = async (newImage) => {
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

    const updateImageAsync = async (updatedImage) => {
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

    const deleteImageAsync = async (imageId) => {
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
        loadImagesOfCollectionAsync,
        addImageAsync,
        updateImageAsync,
        deleteImageAsync
    }
}