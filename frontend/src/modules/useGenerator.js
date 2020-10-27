import { ref, readonly, reactive } from "vue"
import endpoints from "@/services/http/endpoints"
import http from "@/services/http"
import { getCookie } from "@/services/cookie"

/** Status of the generator */
const isGenerating = ref(false);

/**
 * Object that holds the information of a generated image
 */
const image = reactive({
    seed: null,
    filename: null,
    path: null,
});

/**
 * Object that holds previously generated images,
 * those images should not be changed or manipulated
 * just readonly.
 */
const activity = ref([]);

/**
 * Maps an image either from the API or image from the
 * history to the reactive image container
 * @param {*} img {Object}
 */
function mapImage(img) {
    image.seed = img.seed;
    image.filename = img.filename;
    image.path = img.path;
}

export default function useGenerator() {

    const initGenerator = async () => {
        await http.generator.initialize();
    }

    const generate = async (request) => {
        isGenerating.value = true;
        const requestJson = JSON.stringify(request);
        const generatedImage = await http.generator.generate(requestJson);
        if (generatedImage) {
            generatedImage.path = `${endpoints.baseAddress}${endpoints.sessionImages}/${generatedImage.filename}`
            mapImage(generatedImage);
            activity.value.unshift(Object.assign({}, image));
        }
        isGenerating.value = false;
    }

    const loadActivity = async () => {
        const sessionGuid = getCookie("session");
        const sessionActivity = await http.generator.getActivity(sessionGuid);
        console.log(sessionActivity);
        // if (sessionHistory) {

        // }
    }

    const swapImage = (index) => {
        mapImage(activity[index])
    }

    return {
        image: readonly(image),
        isGenerating: readonly(isGenerating),
        activity: readonly(activity),
        initGenerator,
        loadActivity,
        generate,
        swapImage
    }
}