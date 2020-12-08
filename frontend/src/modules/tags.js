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
        } catch (e) {
            notification.error("Failed to load tags", e.message);
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
        } catch (e) {
            notification.error("Failed to load tags for research", e.message);
        } finally {
            researchTagsLoadLock.release();
        }
    }

    const createTagAsync = async (newTag) => {
        try {
            const tagJson = JSON.stringify(newTag);
            const tag = await api.tags.create(tagJson);
            if (tag) {
                tagsById[tag.id] = tag;
            }
        } catch (e) {
            notification.error("Failed to create the tag", e.message);
        }
    }

    const updateTagAsync = async (updatedTag) => {
        try {
            const tagJson = JSON.stringify(updatedTag);
            const tag = await api.tags.update(updatedTag.id, tagJson);
            if (tag) {
                tagsById[tag.id] = tag;
            }
        } catch (e) {
            notification.error("Failed to update the tag", e.message);
        }
    }

    const deleteTagAsync = async (tagId) => {
        try {
            const tag = await api.tags.destroy(tagId);
            if (tag) {
                delete tagsById[tag.id];
            }
        } catch (e) {
            notification.error("Failed to delete the tag", e.message);
        }
    }

    return {
        tagsById: readonly(tagsById),
        researchTagsById: readonly(researchTagsById),
        loadTagsAsync,
        loadResearchTagsAsync,
        createTagAsync,
        updateTagAsync,
        deleteTagAsync
    }
}