import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"

const isGenerating = ref(false);
const initializing = ref(false);
const initialized = ref(false);

const emotions = reactive({});

const currentImage = reactive({
    seed: "",
    filename: "",
    path: "",
});

const activityLoaded = ref(false);
const generatedImages = reactive([]);

function mapImage(image) {
    currentImage.seed = image.seed;
    currentImage.filename = image.filename;
    currentImage.path = image.path;
}

export default function useGenerator() {

    const initGenerator = async () => {
        if (initializing.value || initialized.value) {
            return;
        }
        try {
            initializing.value = true;
            const response = await api.generator.initialize();
            if (response) {
                response.emotions.forEach(emotion => {
                    emotions[emotion.id] = emotion;
                });
                initialized.value = true;
                notification.generator.loaded();
            }
        } catch (e) {
            notification.generator.failedToLoad();
        } finally {
            initializing.value = false;
        }
    }

    const generate = async (request) => {
        try {
            isGenerating.value = true;
            const requestJson = JSON.stringify(request);
            console.log(requestJson)
            const generatedImage = await api.generator.generate(requestJson);
            if (generatedImage) {
                mapImage(generatedImage);
                generatedImages.unshift(generatedImage);
            }
            isGenerating.value = false;
        } catch (e) {
            notification.generator.failedToGenerate();
        }
    }

    const loadActivity = async () => {
        try {
            if (generatedImages !== undefined && activityLoaded.value) {
                return;
            }
            const sessionActivity = await api.generator.getActivity();
            if (sessionActivity) {
                sessionActivity.forEach(image => {
                    generatedImages.push(image);
                });
                activityLoaded.value = true;
            }
        } catch (e) {
            notification.generator.failedToLoadActivity();
        }
    }

    const swapImage = (index) => {
        mapImage(generatedImages[index])
    }

    return {
        currentImage: readonly(currentImage),
        isGenerating: readonly(isGenerating),
        generatedImages: readonly(generatedImages),
        emotions: readonly(emotions),
        initGenerator,
        loadActivity,
        generate,
        swapImage
    }
}