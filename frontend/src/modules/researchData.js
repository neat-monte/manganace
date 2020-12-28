import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const generalLock = new AwaitLock();

export default function useResearchData() {

    const getResultsDataAsync = async (settingId) => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getResultsData(settingId);
        } catch (e) {
            notification.error("Failed to load results data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getSessionResultsDataAsync = async (settingId, sessionId) => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getSessionResultsData(settingId, sessionId);
        } catch (e) {
            notification.error("Failed to load session results data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getExportCsvAsync = async (settingId) => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getExportCsv(settingId);
        } catch (e) {
            notification.error("Failed to export the data", e.message);
        } finally {
            generalLock.release();
        }
    }

    return {
        getResultsDataAsync,
        getSessionResultsDataAsync,
        getExportCsvAsync,
    }
}