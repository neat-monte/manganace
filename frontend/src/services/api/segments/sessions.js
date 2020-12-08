import { fetchJSON, methods } from './base'

const sessionsEndpoint = "/sessions";

export const getAllGenerator = async () => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.GET);
}

export const createGenerator = async (data) => {
    return await fetchJSON(`${sessionsEndpoint}/generator`, methods.POST, data);
}

export const updateGenerator = async (id, data) => {
    return await fetchJSON(`${sessionsEndpoint}/generator/${id}`, methods.PUT, data);
}

export const destroyGenerator = async (id) => {
    return await fetchJSON(`${sessionsEndpoint}/generator/${id}`, methods.DELETE);
}

export const getAllResearch = async () => {
    return await fetchJSON(`${sessionsEndpoint}/research/`, methods.GET);
}

export const createResearch = async (data) => {
    return await fetchJSON(`${sessionsEndpoint}/research/`, methods.POST, data);
}

export const getImages = async (id) => {
    return await fetchJSON(`${sessionsEndpoint}/${id}/images`, methods.GET);
}