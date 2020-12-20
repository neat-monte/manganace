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
    imagesByCollectionId[image.collectionId][image.id] = image
}

export default function useCollectionImages() {

    const loadImagesOfCollectionAsync = async (collectionId) => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded(collectionId)) {
                return;
            }
            const images = await api.collections.getImages(collectionId);
            images.forEach(image => insertImage(image));
            hasLoaded[collectionId] = true;
        } catch (e) {
            notification.error("Failed to load images", e.message);
        } finally {
            loadLock.release();
        }
    }

    const createCollectionImageAsync = async (newImage) => {
        try {
            const imageJson = JSON.stringify(newImage);
            const image = await api.collections.createCImage(imageJson);
            if (image) {
                insertImage(image)
            }
        } catch (e) {
            notification.error("Failed to save the image", e.message);
        }
    }

    const updateCollectionImageAsync = async (updatedImage) => {
        try {
            const imageJson = JSON.stringify(updatedImage);
            const image = await api.collections.updateCImage(updatedImage.id, imageJson)
            if (image) {
                insertImage(image)
            }
        } catch (e) {
            notification.error("Failed to update the image", e.message);
        }
    }

    const deleteCollectionImageAsync = async (imageId) => {
        try {
            const image = await api.collections.destroyCImage(imageId);
            if (image) {
                delete imagesByCollectionId[image.collectionId][image.id];
            }
        } catch (e) {
            notification.error("Failed to delete the image", e.message);
        }
    }

    return {
        imagesByCollectionId: readonly(imagesByCollectionId),
        loadImagesOfCollectionAsync,
        createCollectionImageAsync,
        updateCollectionImageAsync,
        deleteCollectionImageAsync
    }
}