import { error } from './base';

export const failedToLoadGenders = () => {
    const message = "Failed to load genders";
    const description = "The request to load gender options failed...";
    error(message, description);
}

export const failedToLoadEducations = () => {
    const message = "Failed to load educations";
    const description = "The request to load education options failed...";
    error(message, description);
}