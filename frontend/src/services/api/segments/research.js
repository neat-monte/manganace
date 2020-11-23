import { fetchJSON, fetchBlob, methods } from './base'

const researchEndpoint = "/research";

export const assignParticipant = async (data) => {
    return await fetchJSON(`${researchEndpoint}/participant`, methods.POST, data);
}

export const getTrialsMeta = async (sessionId) => {
    return await fetchJSON(`${researchEndpoint}/${sessionId}/trials`, methods.GET);
}

export const getTrialImages = async (data) => {
    return await fetchJSON(`${researchEndpoint}/trial-images`, methods.POST, data);
}

export const getResultsData = async () => {
    return await fetchJSON(`${researchEndpoint}/data`, methods.GET);
}

export const getExportCsv = async () => {
    return await fetchBlob(`${researchEndpoint}/data/export`, methods.GET);
}
