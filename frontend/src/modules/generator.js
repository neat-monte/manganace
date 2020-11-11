import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const isInitialized = ref(false);
const initializeLock = new AwaitLock();

const isGenerating = ref(false);
const generateLock = new AwaitLock();

const activityHasLoaded = ref(false);
const activityLock = new AwaitLock();

const generatedImages = reactive([]);
const vectors = reactive({});
const currentImage = reactive({
    seed: "",
    filename: "",
    url: "",
    vectors: [],
});

const setCurrentImage = (image) => {
    currentImage.seed = image.seed;
    currentImage.filename = image.filename;
    currentImage.url = image.url;
    currentImage.vectors = image.vectors;
}

export default function useGenerator() {

    const initGeneratorAsync = async () => {
        await initializeLock.acquireAsync();
        try {
            if (isInitialized.value) {
                return;
            }
            const response = await api.generator.initialize();
            if (response) {
                response.vectors.forEach(vector => {
                    vectors[vector.id] = vector;
                });
                isInitialized.value = true;
                notification.generator.loaded();
            }
        } catch (e) {
            notification.generator.failedToLoad();
        } finally {
            initializeLock.release();
        }
    }

    const generateAsync = async (request) => {
        await generateLock.acquireAsync();
        try {
            isGenerating.value = true;
            const requestJson = JSON.stringify(request);
            const generatedImage = await api.generator.generate(requestJson);
            if (generatedImage) {
                setCurrentImage(generatedImage);
                generatedImages.unshift(generatedImage);
            }
        } catch (e) {
            notification.generator.failedToGenerate();
        } finally {
            isGenerating.value = false;
            generateLock.release();
        }
    }

    const loadActivityAsync = async () => {
        await activityLock.acquireAsync();
        try {
            if (activityHasLoaded.value) {
                return;
            }
            const sessionActivity = await api.generator.getActivity();
            if (sessionActivity) {
                sessionActivity.forEach(image => {
                    generatedImages.push(image);
                });
                activityHasLoaded.value = true;
            }
        } catch (e) {
            notification.generator.failedToLoadActivity();
        } finally {
            activityLock.release();
        }
    }

    const swapImage = (index) => {
        setCurrentImage(generatedImages[index])
    }

    return {
        currentImage: readonly(currentImage),
        isGenerating: readonly(isGenerating),
        generatedImages: readonly(generatedImages),
        vectors: readonly(vectors),
        initGeneratorAsync,
        loadActivityAsync,
        generateAsync,
        swapImage
    }
}