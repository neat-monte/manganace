import { error } from './base';

export const failedToLoad = () => {
    const message = "Failed to load activity";
    const description = "The request to load activity failed...";
    error(message, description);
}
