import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import moment from "moment"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadLock = new AwaitLock();

const researchSettingsById = reactive({});

const currentResearchSetting = reactive({});

const insertResearchSetting = (setting) => {
    setting.created = moment(setting.created).format("DD-MM-YYYY HH:mm");
    researchSettingsById[setting.id] = setting;
}

export default function useResearchSettings() {

    const loadResearchSettingsAsync = async () => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const settings = await api.research.getResearchSettings();
            settings.forEach(setting => insertResearchSetting(setting));
            hasLoaded.value = true;
        } catch (e) {
            notification.error("Failed to load research settings", e.message);
        } finally {
            loadLock.release();
        }
    }

    const createResearchSettingAsync = async (newSetting) => {
        try {
            const settingJson = JSON.stringify(newSetting);
            const setting = await api.research.createResearchSetting(settingJson);
            if (setting) {
                insertResearchSetting(setting);
            }
        } catch (e) {
            notification.error("Failed to create the research setting", e.message);
        }
    }

    const deleteResearchSettingAsync = async (settingId) => {
        try {
            const setting = await api.research.destroyResearchSetting(settingId);
            if (setting) {
                delete researchSettingsById[setting.id];
            }
        } catch (e) {
            notification.error("Failed to delete the research setting", e.message)
        }
    }

    const setCurrentResearchSetting = (settingId) => {
        const setting = researchSettingsById[settingId];
        if (setting) {
            Object.assign(currentResearchSetting, setting)
        }
    }

    return {
        researchSettingsById: readonly(researchSettingsById),
        currentResearchSetting: readonly(currentResearchSetting),
        loadResearchSettingsAsync,
        createResearchSettingAsync,
        deleteResearchSettingAsync,
        setCurrentResearchSetting
    }
}