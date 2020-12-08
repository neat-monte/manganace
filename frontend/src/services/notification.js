import { notification } from "ant-design-vue";


const send = (type, message, description, placement) => {
    notification[type]({ message, description, placement });
}

export const success = (message, description, placement = "bottomRight") => {
    send("success", message, description, placement);
}

export const warning = (message, description, placement = "bottomRight") => {
    send("warning", message, description, placement);
}

export const error = (message, description, placement = "bottomRight") => {
    send("error", message, description, placement);
}

export default {
    success,
    warning,
    error
}