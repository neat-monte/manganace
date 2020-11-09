import { fetchJSON, methods, buildUrlParams } from './base'

const generatorEndpoint = "/generator";
const generationActivityEndpoint = `${generatorEndpoint}/activity`;

export const initialize = async () => {
  return await fetchJSON(generatorEndpoint, methods.GET);
}

export const generate = async (data) => {
  return await fetchJSON(generatorEndpoint, methods.POST, data);
}

export const getActivity = async (sessionGuid) => {
  const params = { session: sessionGuid };
  const url = buildUrlParams(generationActivityEndpoint, params);
  return await fetchJSON(url)
}