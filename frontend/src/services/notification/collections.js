import { success } from './base';

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