import { reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const loaded = reactive({});
const hasLoaded = (sessionId) => loaded !== undefined && sessionId in loaded && loaded[sessionId]
const activityLock = new AwaitLock();

const imagesBySessionId = reactive({});

const insertImage = (image) => {
    if (imagesBySessionId[image.sessionId] === undefined) {
        imagesBySessionId[image.sessionId] = [];
    }
    imagesBySessionId[image.sessionId].unshift(image);
}

export default function useActivity() {

    const loadImagesOfSessionAsync = async (sessionId) => {
        await activityLock.acquireAsync();
        try {
            if (hasLoaded(sessionId)) {
                return;
            }
            const images = await api.sessions.getImages(sessionId);
            images.forEach(image => insertImage(image));
            loaded[sessionId] = true;
        } catch {
            notification.activity.failedToLoad();
        } finally {
            activityLock.release();
        }
    }

    const addGeneratedImage = async (image) => {
        if (!hasLoaded(image.sessionId)) {
            await loadImagesOfSessionAsync();
        }
        await activityLock.acquireAsync();
        try {
            insertImage(image);
        } finally {
            activityLock.release();
        }
    }

    const deleteImage = async (sessionId, image) => {
        await activityLock.acquireAsync();
        try {
            await api.images.destroyImage(image.id);
            const index = imagesBySessionId[sessionId].indexOf(image);
            if (index > -1) {
                imagesBySessionId[sessionId].splice(index, 1);
            }
        } catch (e) {
            if (e.message === "Forbidden") {
                notification.activity.cannotDeleteImage();
            } else {
                notification.activity.failedToDeleteImage();
            }
        }
        finally {
            activityLock.release();
        }
    }

    return {
        imagesBySessionId: readonly(imagesBySessionId),
        loadImagesOfSessionAsync,
        addGeneratedImage,
        deleteImage,
    }
}