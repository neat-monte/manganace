const domain = "http://localhost:8000";

/**
 * Fetch pipeline function which validates if the response is OK [status = 200]
 * @param response
 * @returns {{ok}|*}
 */
async function validate(response) {
  if (!response.ok) {
    const errorBody = await response.json();
    if (errorBody.detail) {
      throw Error(`[${response.status}] ${response.statusText} | ${errorBody.detail} | URL: ${response.url}`);
    }
    throw Error(`[${response.status}] ${response.statusText} | URL: ${response.url}`)
  }
  return response;
}

/**
 * Fetch pipeline function which converts response to JSON
 * @param response
 * @returns {*}
 */
function jsonify(response) {
  return response.json();
}

/**
 * Fetch pipeline function which converts response to Blob object
 * @param {*} response 
 */
function blobify(response) {
  return response.blob();
}

/**
 * Fetch pipeline function which logs an error
 * @param error
 */
function dump(error) {
  console.error(`There was a problem: \n ${error.message}`);
  const start = error.message.indexOf('|');
  const end = error.message.indexOf('|', start + 1);
  if (start >= 0 && end >= 0) {
    throw Error(error.message.substring(start + 2, end - 1));
  }
  throw Error(error.message.substring(0, start));
}

function checkUrl(url) {
  if ((typeof url === "string" || url instanceof String) && !url.startsWith(domain)) {
    return `${domain}${url}`;
  }
  return url;
}

/**
 * Wrapped fetch call with a predetermined pipeline to validate and convert to JSON,
 * and in case of error - log to the console and throw an error
 * @param url {String|URL}
 * @param method {String}
 * @param data {*}
 * @returns {Promise<postcss.Result|any|undefined>}
 */
export async function fetchJSON(url, method, data = null) {
  url = checkUrl(url);
  return await fetch(url, { method: method, body: data })
    .then(validate)
    .then(jsonify)
    .catch(dump);
}

/**
 * Wrapped fetch call with a predetermined pipeline to validate and convert to Blob,
 * and in case of error - log to the console and throw an error
 * @param url {String|URL}
 * @param method {String}
 * @returns {Promise<postcss.Result|any|undefined>}
 */
export async function fetchBlob(url, method, data = null) {
  url = checkUrl(url);
  return await fetch(url, { method: method, body: data })
    .then(validate)
    .then(blobify)
    .catch(dump);
}

/**
 * Enumeration of viable fetch methods
 * @type {{DELETE: string, POST: string, GET: string, PUT: string}}
 */
export const methods = {
  GET: 'GET',
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE'
}

/**
 * Builds a URL object with query parameters
 * @param endpoint {String}
 * @param params {*}
 * @returns {URL}
 */
export function buildUrlParams(endpoint, params) {
  const address = `${domain}${endpoint}`;
  const url = new URL(address);
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
  return url;
}
