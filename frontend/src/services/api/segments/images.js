import { fetchJSON as fetchJSON, methods } from './base'

const collectionImagesEndpoint = "/collections/images";
const imagesEndpoint = "/images";

export const createCImage = async (data) => {
  return await fetchJSON(collectionImagesEndpoint, methods.POST, data);
}

export const updateCImage = async (id, data) => {
  return await fetchJSON(`${collectionImagesEndpoint}/${id}`, methods.PUT, data);
}

export const destroyCImage = async (id) => {
  return await fetchJSON(`${collectionImagesEndpoint}/${id}`, methods.DELETE);
}

export const destroyImage = async (id) => {
  return await fetchJSON(`${imagesEndpoint}/${id}`, methods.DELETE);
}

export const createTrialPick = async (data) => {
  console.log(data);
  return await fetchJSON(`${collectionImagesEndpoint}/trial`, methods.POST, data);
}