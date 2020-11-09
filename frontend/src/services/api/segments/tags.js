import { fetchJSON, methods } from './base'

const tagsEndpoint = "/tags";

export const getAll = async () => {
  return await fetchJSON(tagsEndpoint, methods.GET);
}

export const create = async (data) => {
  return await fetchJSON(tagsEndpoint, methods.POST, data);
}

export const update = async (id, data) => {
  return await fetchJSON(`${tagsEndpoint}/${id}`, methods.PUT, data);
}

export const destroy = async (id) => {
  return await fetchJSON(`${tagsEndpoint}/${id}`, methods.DELETE);
}