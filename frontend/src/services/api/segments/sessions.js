import { fetchJSON, methods } from './base'

const sessionsEndpoint = "/sessions";

/* Research sessions */

export const getAllResearch = async (settingId) => {
    return await fetchJSON(`${sessionsEndpoint}/research/${settingId}`, methods.GET);
}

export const createResearch = async (settingId, data) => {
    return await fetchJSON(`${sessionsEndpoint}/research/${settingId}`, methods.POST, data);
}

/* Generator sessions */

export const getAllGenerator = async () => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.GET);
}

export const createGenerator = async (data) => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.POST, data);
}

/* Images (any session) */

export const getImages = async (sessionId) => {
    return await fetchJSON(`${sessionsEndpoint}/${sessionId}/images`, methods.GET);
}

export const destroyImage = async (imageId) => {
    return await fetchJSON(`${sessionsEndpoint}/images/${imageId}`, methods.DELETE);
}