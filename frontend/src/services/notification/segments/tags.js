import { success, error } from './base';

export const created = (entity) => {
    const message = "Tag created";
    const description = `Tag "${entity.name}" was created successfully`
    success(message, description);
}

export const updated = (entity) => {
    const message = "Tag updated";
    const description = `Tag "${entity.name}" was updated successfully`
    success(message, description);
}

export const deleted = (entity) => {
    const message = "Tag deleted";
    const description = `Tag "${entity.name}" was deleted successfully`
    success(message, description);
}

export const failedToLoad = () => {
    const message = "Failed to load tags";
    const description = "The request to load tags failed...";
    error(message, description);
}

export const failedToLoadResearchTags = () => {
    const message = "Failed to load research tags";
    const description = "The request to load research tags failed...";
    error(message, description);
}

export const failedToAdd = () => {
    const message = "Failed to add tag";
    const description = "The request to add new tag failed...";
    error(message, description);
}

export const failedToUpdate = () => {
    const message = "Failed to update tag";
    const description = "The request to update tag failed...";
    error(message, description);
}

export const failedToDelete = () => {
    const message = "Failed to delete tag";
    const description = "The request to delete tag failed...";
    error(message, description);
}
