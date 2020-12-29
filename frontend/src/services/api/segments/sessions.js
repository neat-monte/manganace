import { fetchJSON, methods } from './base'

const sessionsEndpoint = "/sessions";

/* Research sessions */

export const getAllResearch = async (settingId) => {
    return await fetchJSON(`${sessionsEndpoint}/research/${settingId}`, methods.GET);
}

export const createResearch = async (data) => {
    return await fetchJSON(`${sessionsEndpoint}/research/setting`, methods.POST, data);
}

export const destroyResearch = async (sessionId) => {
    return await fetchJSON(`${sessionsEndpoint}/research/setting/${sessionId}`, methods.DELETE)
}

/* Generator sessions */

export const getAllGenerator = async () => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.GET);
}

export const createGenerator = async (data) => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.POST, data);
}

export const destroyGenerator = async (sessionId) => {
    return await fetchJSON(`${sessionsEndpoint}/generator/${sessionId}`, methods.DELETE)
}

/* Images (any session) */

export const getImages = async (sessionId) => {
    return await fetchJSON(`${sessionsEndpoint}/${sessionId}/images`, methods.GET);
}

export const destroyImage = async (imageId) => {
    return await fetchJSON(`${sessionsEndpoint}/images/${imageId}`, methods.DELETE);
}