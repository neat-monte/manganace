import { ref, reactive, readonly } from "vue"
import endpoints from "@/services/http/endpoints"
import http from "@/services/http"

const generating = ref(false);

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

    const generate = async (request) => {
        generating.value = true;
        const requestJson = JSON.stringify(request);
        const generatedImage = await http.generator.generate(requestJson);
        if (generatedImage) {
            mapImage(generatedImage);
            state.history.unshift(Object.assign({}, state.image));
        }
        generating.value = false;
    }

    return {
        state: readonly(state),
        initGenerator,
        generate,
        generating
    }
}