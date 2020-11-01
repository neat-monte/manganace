import { success, error } from './base';

export const created = (entity) => {
    const message = "Collection created";
    const description = `Collection "${entity.name}" was created successfully`
    success(message, description);
}

export const updated = (entity) => {
    const message = "Collection updated";
    const description = `Collection "${entity.name}" was updated successfully`
    success(message, description);
}

export const deleted = (entity) => {
    const message = "Collection deleted";
    const description = `Collection "${entity.name}" was deleted successfully`
    success(message, description);
}

export const failedToLoad = () => {
    const message = "Failed to load collections";
    const description = "The request to load collections failed...";
    error(message, description);
}

export const failedToAdd = () => {
    const message = "Failed to add collection";
    const description = "The request to add new collection failed...";
    error(message, description);
}

export const failedToUpdate = () => {
    const message = "Failed to update collection";
    const description = "The request to update collection failed...";
    error(message, description);
}

export const failedToDelete = () => {
    const message = "Failed to delete collection";
    const description = "The request to delete collection failed...";
    error(message, description);
}





