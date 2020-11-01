import { ref, readonly, reactive } from "vue"
import http from "@/services/http"
import { getCookie } from "@/services/cookie"
import notification from "@/services/notification"

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

export default function useGenerator() {

    const initGenerator = async () => {
        await http.generator.initialize();
        activity.session = getCookie("session");
        notification.generator.loaded();
    }

    const generate = async (request) => {
        isGenerating.value = true;
        const requestJson = JSON.stringify(request);
        const generatedImage = await http.generator.generate(requestJson);
        if (generatedImage) {
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