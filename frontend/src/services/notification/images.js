import { success } from './base';

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