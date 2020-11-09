import { success, error } from './base';


export const loaded = () => {
    const message = "Generator is ready";
    const description = "The generator was started successfully";
    success(message, description);
}

export const failedToLoad = () => {
    const message = "Failed to load generator";
    const description = "The request to load the generator failed...";
    error(message, description);
}

export const failedToGenerate = () => {
    const message = "Failed to generate an image";
    const description = "The request to generate an image failed...";
    error(message, description);
}

export const failedToLoadActivity = () => {
    const message = "Failed to load activity";
    const description = "The request to retrieve the session activity failed...";
    error(message, description);
}