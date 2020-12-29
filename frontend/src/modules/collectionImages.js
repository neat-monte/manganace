import { reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import useResearchSessions from "./researchSessions";
import AwaitLock from 'await-lock';

const { incrementProgress } = useResearchSessions();

const loaded = reactive({});
const hasLoaded = (collectionId) => loaded !== undefined && collectionId in loaded && loaded[collectionId]
const loadLock = new AwaitLock();

const imagesByCollectionId = reactive({});

const insertImage = (image) => {
    if (imagesByCollectionId[image.collectionId] === undefined) {
        imagesByCollectionId[image.collectionId] = [];
    }
    const prevImage = imagesByCollectionId[image.collectionId].filter(i => i.id === image.id)[0];
    if (prevImage) {
        Object.assign(prevImage, image)
    } else {
        imagesByCollectionId[image.collectionId].push(image);
    }
}

export default function useCollectionImages() {

    const loadImagesOfCollectionAsync = async (collectionId) => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded(collectionId)) {
                return;
            }
            const images = await api.collections.getImages(collectionId);
            imagesByCollectionId[collectionId] = [];
            images.forEach(image => insertImage(image));
            hasLoaded[collectionId] = true;
        } catch (e) {
            notification.error("Failed to load images", e.message);
        } finally {
            loadLock.release();
        }
    }

    const createCollectionImageAsync = async (newImage) => {
        console.log("test");
        try {
            const imageJson = JSON.stringify(newImage);
            const image = await api.collections.createImage(imageJson);
            insertImage(image);
        } catch (e) {
            notification.error("Failed to save the image", e.message);
        }
    }

    const updateCollectionImageAsync = async (updatedImage) => {
        try {
            const imageJson = JSON.stringify(updatedImage);
            const image = await api.collections.updateImage(updatedImage.id, imageJson)
            insertImage(image);
        } catch (e) {
            notification.error("Failed to update the image", e.message);
        }
    }

    const deleteCollectionImageAsync = async (imageId) => {
        try {
            const image = await api.collections.destroyImage(imageId);
            const index = imagesByCollectionId[image.collectionId].indexOf(image);
            imagesByCollectionId[image.collectionId].splice(index, 1);
        } catch (e) {
            notification.error("Failed to delete the image", e.message);
        }
    }

    const createTrialPickAsync = async (chosenImage) => {
        try {
            const imageJson = JSON.stringify(chosenImage);
            await api.collections.createTrialPick(imageJson);
            incrementProgress();
        } catch (e) {
            notification.error("Failed to save the answer", e.message);
        }
    }

    return {
        imagesByCollectionId: readonly(imagesByCollectionId),
        loadImagesOfCollectionAsync,
        createCollectionImageAsync,
        updateCollectionImageAsync,
        deleteCollectionImageAsync,
        createTrialPickAsync
    }
}