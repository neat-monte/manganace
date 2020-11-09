import { fetchJSON, methods } from './base'

const collectionsEndpoint = "/collections";

export const getAll = async () => {
  return await fetchJSON(collectionsEndpoint, methods.GET);
}

export const create = async (data) => {
  return await fetchJSON(collectionsEndpoint, methods.POST, data);
}

export const update = async (id, data) => {
  return await fetchJSON(`${collectionsEndpoint}/${id}`, methods.PUT, data);
}

export const destroy = async (id) => {
  return await fetchJSON(`${collectionsEndpoint}/${id}`, methods.DELETE);
}

export const getImagesOfCollecton = async (id) => {
  return await fetchJSON(`${collectionsEndpoint}/${id}/images`, methods.GET);
}