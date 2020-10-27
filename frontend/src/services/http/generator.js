import endpoints from './endpoints'
import { fetchAsync, sendAsync, methods, buildUrlParams } from './base'

export const initialize = async () => {
  return await sendAsync(endpoints.generator, methods.GET);
}

export const generate = async (data) => {
  return await fetchAsync(endpoints.generator, methods.POST, data);
}

export const getActivity = async (sessionGuid) => {
  const params = { session: sessionGuid };
  const url = buildUrlParams(endpoints.getActivity, params);
  return await fetchAsync(url)
}