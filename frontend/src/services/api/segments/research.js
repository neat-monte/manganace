import { fetchJSON, fetchBlob, methods } from './base'

const researchEndpoint = "/research";

/* Research data */

export const getResultsData = async (settingId) => {
    return await fetchJSON(`${researchEndpoint}/${settingId}/data`, methods.GET);
}

export const getSessionResultsData = async (settingId, sessionId) => {
    return await fetchJSON(`${researchEndpoint}/${settingId}/data/${sessionId}`, methods.GET);
}

export const getExportCsv = async (settingId) => {
    return await fetchBlob(`${researchEndpoint}/${settingId}/data/export`, methods.GET);
}

/* Research trials */

export const getTrialsMeta = async (sessionId) => {
    return await fetchJSON(`${researchEndpoint}/${sessionId}/trials`, methods.GET);
}

export const getTrialImages = async (data) => {
    return await fetchJSON(`${researchEndpoint}/trial/images`, methods.POST, data);
}

/* Research participants */

export const assignParticipant = async (data) => {
    return await fetchJSON(`${researchEndpoint}/participants`, methods.POST, data);
}

/* Research settings */

export const getResearchSettings = async () => {
    return await fetchJSON(`${researchEndpoint}/settings`, methods.GET);
}

export const createResearchSetting = async (data) => {
    return await fetchJSON(`${researchEndpoint}/settings`, methods.POST, data);
}

export const destroyResearchSetting = async (settingId) => {
    return await fetchJSON(`${researchEndpoint}/settings/${settingId}`, methods.DELETE);
}