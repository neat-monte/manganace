import { success, error } from './base';

export const added = () => {
    const message = "Image added ";
    const description = `Image was added successfully`
    success(message, description);
}

export const updated = () => {
    const message = "Image updated";
    const description = `Image was updated successfully`
    success(message, description);
}

export const deleted = () => {
    const message = "Image deleted";
    const description = `Image was deleted successfully`
    success(message, description);
}

export const failedToLoad = () => {
    const message = "Failed to load images";
    const description = "The request to load images failed...";
    error(message, description);
}

export const failedToSave = () => {
    const message = "Failed to save image";
    const description = "The request to save the image failed...";
    error(message, description);
}

export const failedToUpdate = () => {
    const message = "Failed to update image";
    const description = "The request to update image failed...";
    error(message, description);
}

export const failedToDelete = () => {
    const message = "Failed to delete image";
    const description = "The request to delete image failed...";
    error(message, description);
}
