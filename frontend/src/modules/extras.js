import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const gendersLoaded = ref(false);
const gendersLoadLock = new AwaitLock();

const educationsLoaded = ref(false);
const educationsLoadLock = new AwaitLock();

const researchTagsLoaded = ref(false);
const researchTagsLoadLock = new AwaitLock();

const gendersById = reactive({});
const educationsById = reactive({});
const researchTagsById = reactive({});

export default function useExtras() {

    const loadGendersAsync = async () => {
        await gendersLoadLock.acquireAsync();
        try {
            if (gendersLoaded.value) {
                return;
            }
            const genders = await api.extras.getGendersOptions();
            if (genders) {
                genders.forEach(gen => gendersById[gen.id] = gen);
                gendersLoaded.value = true;
            }
        } catch {
            notification.extras.failedToLoadGenders();
        } finally {
            gendersLoadLock.release();
        }
    }

    const loadEducationsAsync = async () => {
        await educationsLoadLock.acquireAsync();
        try {
            if (educationsLoaded.value) {
                return;
            }
            const educations = await api.extras.getEducationsOptions();
            if (educations) {
                educations.forEach(edu => educationsById[edu.id] = edu);
                educationsLoaded.value = true;
            }
        } catch {
            notification.extras.failedToLoadEducations();
        } finally {
            educationsLoadLock.release();
        }
    }

    const loadResearchTagsAsync = async () => {
        await researchTagsLoadLock.acquireAsync();
        try {
            if (researchTagsLoaded.value) {
                return;
            }
            const tags = await api.tags.getResearchTags();
            if (tags) {
                tags.forEach(tags => researchTagsById[tags.id] = tags);
                researchTagsLoaded.value = true;
            }
        } catch {
            notification.tags.failedToLoadResearchTags();
        } finally {
            researchTagsLoadLock.release();
        }
    }

    return {
        gendersById: readonly(gendersById),
        educationsById: readonly(educationsById),
        researchTagsById: readonly(researchTagsById),
        loadGendersAsync,
        loadEducationsAsync,
        loadResearchTagsAsync
    }
}