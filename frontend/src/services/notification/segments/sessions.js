import { success, error } from './base';

export const created = (entity) => {
    const message = "Session created";
    const description = `Session "${entity.name}" was created successfully`
    success(message, description);
}

export const updated = (entity) => {
    const message = "Session updated";
    const description = `Session "${entity.name}" was updated successfully`
    success(message, description);
}

export const deleted = (entity) => {
    const message = "Session deleted";
    const description = `Session "${entity.name}" was deleted successfully`
    success(message, description);
}

export const failedToLoad = () => {
    const message = "Failed to load sessions";
    const description = "The request to load sessions failed...";
    error(message, description);
}

export const failedToAdd = () => {
    const message = "Failed to add session";
    const description = "The request to add new session failed...";
    error(message, description);
}

export const failedToUpdate = () => {
    const message = "Failed to update session";
    const description = "The request to update session failed...";
    error(message, description);
}

export const failedToDelete = () => {
    const message = "Failed to delete session";
    const description = "The request to delete session failed...";
    error(message, description);
}

export const cannotAssignParticipant = () => {
    const message = "Cannot assign participant";
    const description = "Either the provided session does not exist or participant is already assigned...";
    error(message, description);
}

export const failedToAssignParticipant = () => {
    const message = "Failed to assign participant";
    const description = "The request to assign participant failed...";
    error(message, description);
}