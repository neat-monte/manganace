import { ref, reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadLock = new AwaitLock();

const researchTagsLoaded = ref(false);
const researchTagsLoadLock = new AwaitLock();

const tagsById = reactive({});
const researchTagsById = reactive({});

export default function useTags() {

    const loadTagsAsync = async () => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const tags = await api.tags.getAll();
            if (tags) {
                tags.forEach(tag => tagsById[tag.id] = tag);
                hasLoaded.value = true;
            }
        } catch {
            notification.tags.failedToLoad();
        } finally {
            loadLock.release();
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

    const addTagAsync = async (newTag) => {
        try {
            const tagJson = JSON.stringify(newTag);
            const tag = await api.tags.create(tagJson);
            if (tag) {
                tagsById[tag.id] = tag;
                notification.tags.created(tag);
            }
        } catch {
            notification.tags.failedToAdd();
        }
    }

    const updateTagAsync = async (updatedTag) => {
        try {
            const tagJson = JSON.stringify(updatedTag);
            const tag = await api.tags.update(updatedTag.id, tagJson);
            if (tag) {
                tagsById[tag.id] = tag;
                notification.tags.updated(tag);
            }
        } catch {
            notification.tags.failedToUpdate();
        }
    }

    const deleteTagAsync = async (tagId) => {
        try {
            const tag = await api.tags.destroy(tagId);
            if (tag) {
                delete tagsById[tag.id];
                notification.tags.deleted(tag);
            }
        } catch {
            notification.tags.failedToDelete();
        }
    }

    return {
        areLoaded: readonly(hasLoaded),
        tagsById: readonly(tagsById),
        researchTagsById: readonly(researchTagsById),
        loadTagsAsync,
        loadResearchTagsAsync,
        addTagAsync,
        updateTagAsync,
        deleteTagAsync
    }
}