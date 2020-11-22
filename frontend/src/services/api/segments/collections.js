import { fetchJSON, methods } from './base'

const collectionsEndpoint = "/collections";

export const getAllUser = async () => {
  return await fetchJSON(`${collectionsEndpoint}/user`, methods.GET);
}

export const createUser = async (data) => {
  return await fetchJSON(`${collectionsEndpoint}/user`, methods.POST, data);
}

export const updateUser = async (id, data) => {
  return await fetchJSON(`${collectionsEndpoint}/user/${id}`, methods.PUT, data);
}

export const destroyUser = async (id) => {
  return await fetchJSON(`${collectionsEndpoint}/user/${id}`, methods.DELETE);
}

export const getImages = async (id) => {
  return await fetchJSON(`${collectionsEndpoint}/${id}/images`, methods.GET);
}