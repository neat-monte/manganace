import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const generalLock = new AwaitLock();

export default function useResearchTrials() {

    const getTrialsMetaInfoAsync = async (sessionId) => {
        await generalLock.acquireAsync();
        try {
            return await api.research.getTrialsMeta(sessionId)
        } catch (e) {
            notification.error("Failed to load trials data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getTrialImagesAsync = async (trialMeta) => {
        await generalLock.acquireAsync();
        try {
            const trialMetaJson = JSON.stringify(trialMeta);
            return await api.research.getTrialImages(trialMetaJson)
        } catch (e) {
            notification.error("Failed to load images of the trial", e.message);
        } finally {
            generalLock.release();
        }
    }

    return {
        getTrialsMetaInfoAsync,
        getTrialImagesAsync,
    }
}