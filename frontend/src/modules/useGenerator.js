import { ref, readonly, reactive } from "vue"
import endpoints from "@/services/http/endpoints"
import http from "@/services/http"
import { getCookie } from "@/services/cookie"

/**
 * Status of the generator
 */
const isGenerating = ref(false);

/**
 * Object that holds the information of a generated image
 */
const image = reactive({
    seed: "",
    filename: "",
    path: "",
});

/**
 * Object that holds previously generated images,
 * those images should not be changed or manipulated
 * just readonly.
 */
const activity = reactive({
    session: getCookie("session"),
    images: []
});

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

/**
 * Assembles a path attribute for a generated image
 * @param {*} img {Object}
 */
function addPath(img) {
    img.path = `${endpoints.baseAddress}${endpoints.sessionImages}/${activity.session}/${img.filename}`
}

export default function useGenerator() {

    const initGenerator = async () => {
        await http.generator.initialize();
        activity.session = getCookie("session");
    }

    const generate = async (request) => {
        isGenerating.value = true;
        const requestJson = JSON.stringify(request);
        const generatedImage = await http.generator.generate(requestJson);
        if (generatedImage) {
            addPath(generatedImage);
            mapImage(generatedImage);
            activity.images.unshift(generatedImage);
        }
        isGenerating.value = false;
    }

    const loadActivity = async () => {
        if (activity.images !== undefined && activity.images.length > 0) {
            return;
        }
        const sessionActivity = await http.generator.getActivity(activity.session);
        if (sessionActivity) {
            sessionActivity.forEach(image => {
                addPath(image);
                activity.images.push(image);
            });
        }
    }

    const swapImage = (index) => {
        mapImage(activity.images[index])
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