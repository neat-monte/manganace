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

export default function useGeneratorSessionImages() {

    const loadImagesOfSessionAsync = async (sessionId) => {
        await activityLock.acquireAsync();
        try {
            if (hasLoaded(sessionId)) {
                return;
            }
            const images = await api.sessions.getImages(sessionId);
            images.forEach(image => insertImage(image));
            loaded[sessionId] = true;
        } catch (e) {
            notification.error("Failed to load activity", e.message);
        } finally {
            activityLock.release();
        }
    }

    const insertGeneratedImage = async (image) => {
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

    const tryDeleteImageAsync = async (sessionId, image) => {
        await activityLock.acquireAsync();
        try {
            await api.sessions.destroyImage(image.id);
            const index = imagesBySessionId[sessionId].indexOf(image);
            if (index > -1) {
                imagesBySessionId[sessionId].splice(index, 1);
            }
        } catch (e) {
            notification.error("Failed to delete image", e.message)
        }
        finally {
            activityLock.release();
        }
    }

    return {
        imagesBySessionId: readonly(imagesBySessionId),
        loadImagesOfSessionAsync,
        tryDeleteImageAsync,
        insertGeneratedImage,
    }
}