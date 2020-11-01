import { success } from './base';

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