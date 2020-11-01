import { success } from './base';


export const loaded = () => {
    const message = "Generator is ready";
    const description = "Generator was started successfully"
    success(message, description);
}