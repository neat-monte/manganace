import { error, warning } from './base';

export const failedToLoad = () => {
    const message = "Failed to load activity";
    const description = "The request to load activity failed...";
    error(message, description);
}

export const failedToDeleteImage = () => {
    const message = "Failed to delete image";
    const description = "The request to delete the image failed...";
    error(message, description);
}

export const cannotDeleteImage = () => {
    const message = "Cannot delete image";
    const description = "At least one collection is dependent on the image";
    warning(message, description);
}