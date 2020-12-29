import { fetchJSON, methods } from './base'

const collectionsEndpoint = "/collections";

/* User collections */

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

/* Collection images & trial picks */

export const getImages = async (collectionId) => {
  return await fetchJSON(`${collectionsEndpoint}/${collectionId}/images`, methods.GET);
}

export const createImage = async (data) => {
  return await fetchJSON(`${collectionsEndpoint}/images`, methods.POST, data);
}

export const createTrialPick = async (data) => {
  return await fetchJSON(`${collectionsEndpoint}/trial-pick`, methods.POST, data);
}

export const updateImage = async (id, data) => {
  return await fetchJSON(`${collectionsEndpoint}/images/${id}`, methods.PUT, data);
}

export const destroyImage = async (id) => {
  return await fetchJSON(`${collectionsEndpoint}/images/${id}`, methods.DELETE);
}