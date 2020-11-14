import { fetchJSON, methods } from './base'

const sessionsEndpoint = "/sessions";

export const getAll = async () => {
    return await fetchJSON(sessionsEndpoint, methods.GET);
}

export const create = async (data) => {
    return await fetchJSON(sessionsEndpoint, methods.POST, data);
}

export const update = async (id, data) => {
    return await fetchJSON(`${sessionsEndpoint}/${id}`, methods.PUT, data);
}

export const destroy = async (id) => {
    return await fetchJSON(`${sessionsEndpoint}/${id}`, methods.DELETE);
}

export const getImagesOfSession = async (id) => {
    return await fetchJSON(`${sessionsEndpoint}/${id}/images`, methods.GET);
}