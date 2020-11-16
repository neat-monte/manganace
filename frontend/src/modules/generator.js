import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import useActivity from "./activity";
import AwaitLock from 'await-lock';

const { imagesBySessionId, addGeneratedImage } = useActivity();

const isInitialized = ref(false);
const initializeLock = new AwaitLock();

const isGenerating = ref(false);
const generateLock = new AwaitLock();

const currentSession = reactive({});

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
            if (!currentSession.id) {
                notification.generator.selectSessionFirst();
                return;
            }
            request["sessionId"] = currentSession.id;
            const requestJson = JSON.stringify(request);
            const generatedImage = await api.generator.generate(requestJson);
            if (generatedImage) {
                addGeneratedImage(generatedImage);
                setCurrentImage(generatedImage);
            }
        } catch (e) {
            notification.generator.failedToGenerate();
        } finally {
            isGenerating.value = false;
            generateLock.release();
        }
    }

    const setCurrentSession = (session) => {
        if (session && session.id && session.name) {
            currentSession.id = session.id;
            currentSession.name = session.name;
        } else if (session == null) {
            currentSession.id = undefined;
            currentSession.name = undefined;
        }
    }

    const swapImage = (index) => {
        setCurrentImage(imagesBySessionId[currentSession.id][index])
    }

    return {
        currentImage: readonly(currentImage),
        currentSession: readonly(currentSession),
        isGenerating: readonly(isGenerating),
        vectors: readonly(vectors),
        initGeneratorAsync,
        generateAsync,
        setCurrentSession,
        swapImage,
    }
}