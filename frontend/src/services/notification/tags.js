import { success } from './base';

export const created = (entity) => {
    const message = "Tag created";
    const description = `Tag "${entity.name}" was created successfully`
    success(message, description);
}