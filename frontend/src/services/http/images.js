import endpoints from './endpoints'
import { fetchAsync, methods } from './base'

export const getImagesOfCollecton = async (collectionId) => {
  const endpoint = `${endpoints.collections}/${collectionId}/images`;
  return await fetchAsync(endpoint, methods.GET);
}

export const create = async (data) => {
  return await fetchAsync(endpoints.images, methods.POST, data);
}

export const update = async (id, data) => {
  const endpoint = `${endpoints.images}/${id}`
  return await fetchAsync(endpoint, methods.PUT, data);
}

export const destroy = async (id) => {
  const endpoint = `${endpoints.images}/${id}`;
  return await fetchAsync(endpoint, methods.DELETE);
}