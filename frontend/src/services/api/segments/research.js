import { fetchJSON, methods } from './base'

const researchEndpoint = "/research";

export const getSessions = async () => {
    return await fetchJSON(researchEndpoint, methods.GET);
}

export const initializeSession = async (data) => {
    return await fetchJSON(researchEndpoint, methods.POST, data);
}