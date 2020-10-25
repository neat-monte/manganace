import { reactive, readonly } from "vue"
import endpoints from "@/services/http/endpoints"
import http from "@/services/http"

const state = reactive({
    image: {
        seed: null,
        filename: null,
        path: null,
    },
    history: []
});

function mapImage(image) {
    state.image.seed = image.seed;
    state.image.filename = image.filename;
    state.image.path = `${endpoints.baseAddress}${endpoints.static}/${image.filename}`;
}

export default function useGenerator() {

    const initGenerator = async () => {
        await http.generator.initialize();
    }

    const generateImage = async (request) => {
        const requestJson = JSON.stringify(request);
        const generatedImage = await http.generator.generate(requestJson);
        if (generatedImage) {
            mapImage(generatedImage);
            state.history.push(state.image);
        }
    }

    return {
        state: readonly(state),
        initGenerator,
        generateImage
    }
}