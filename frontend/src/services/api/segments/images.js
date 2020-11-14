import { fetchJSON as fetchJSON, methods } from './base'

const imagesEndpoint = "/images";

export const create = async (data) => {
  return await fetchJSON(imagesEndpoint, methods.POST, data);
}

export const update = async (id, data) => {
  return await fetchJSON(`${imagesEndpoint}/${id}`, methods.PUT, data);
}

export const destroy = async (id) => {
  return await fetchJSON(`${imagesEndpoint}/${id}`, methods.DELETE);
}