import { error } from './base';

export const cannotLoadTrialsMetaInfo = () => {
    const message = "Cannot load trials";
    const description = "The session is not assigned...";
    error(message, description);
}

export const failedToLoadTrialsMetaInfo = () => {
    const message = "Failed to load trials meta";
    const description = "The request to load trials meta info failed...";
    error(message, description);
}

export const failedToLoadTrialImages = () => {
    const message = "Failed to load trial images";
    const description = "The request to load trial images failed...";
    error(message, description);
}
