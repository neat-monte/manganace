import { fetchJSON, methods } from './base'

const researchEndpoint = "/research";

export const getSessions = async () => {
    return await fetchJSON(researchEndpoint, methods.GET);
}

export const initializeSession = async (data) => {
    return await fetchJSON(researchEndpoint, methods.POST, data);
}

export const assignParticipant = async (data) => {
    return await fetchJSON(`${researchEndpoint}/participant`, methods.POST, data);
}

export const getTrialsMeta = async (sessionId) => {
    return await fetchJSON(`${researchEndpoint}/${sessionId}/trials`, methods.GET);
}

export const getTrialImages = async (data) => {
    return await fetchJSON(`${researchEndpoint}/trial-images`, methods.POST, data);
}
