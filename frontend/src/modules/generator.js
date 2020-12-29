import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import useGeneratorSessionImages from "./generatorSessionImages";
import AwaitLock from 'await-lock';

const { imagesBySessionId, insertGeneratedImage } = useGeneratorSessionImages();

const isInitialized = ref(false);
const initializeLock = new AwaitLock();

const isGenerating = ref(false);
const generateLock = new AwaitLock();

const vectors = reactive({});
const currentImage = reactive({});

const setCurrentImage = (image) => {
    currentImage.id = image.id;
    currentImage.session_id = image.session_id;
    currentImage.seed = image.seed;
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
            response.vectors.forEach(vector => {
                vectors[vector.id] = vector;
            });
            isInitialized.value = true;
            notification.success("Generator is ready");
        } catch (e) {
            notification.error("Failed to initialize the generator", e.message);
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
            insertGeneratedImage(generatedImage);
            setCurrentImage(generatedImage);
        } catch (e) {
            notification.error("Failed to generate an image", e.message);
        } finally {
            isGenerating.value = false;
            generateLock.release();
        }
    }

    const swapImage = (sessionId, imageIndex) => {
        setCurrentImage(imagesBySessionId[sessionId][imageIndex])
    }

    const nullifyImage = () => {
        Object.keys(currentImage).forEach((k) => currentImage[k] = undefined);
    }

    const usingGeneratorAsync = async () => {
        await generateLock.acquireAsync();
        isGenerating.value = true;
    }

    const finishedUsingGenerator = () => {
        generateLock.release();
        isGenerating.value = false;
    }

    return {
        currentImage: readonly(currentImage),
        isGenerating: readonly(isGenerating),
        vectors: readonly(vectors),
        initGeneratorAsync,
        generateAsync,
        swapImage,
        nullifyImage,
        usingGeneratorAsync,
        finishedUsingGenerator,
    }
}