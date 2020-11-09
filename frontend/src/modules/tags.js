import { ref, reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"

const loaded = ref(false);
const tagsById = reactive({});

function insertTag(tag) {
  tagsById[tag.id] = tag;
}

export default function useTags() {

  const loadTags = async () => {
    if (tagsById !== undefined && loaded.value) {
      return;
    }
    try {
      const tags = await api.tags.getAll();
      if (tags) {
        tags.forEach(tag => insertTag(tag));
      }
    } catch {
      notification.tags.failedToLoad();
    }
  }

  const addTag = async (newTag) => {
    try {
      const tagJson = JSON.stringify(newTag);
      const tag = await api.tags.create(tagJson);
      if (tag) {
        insertTag(tag);
        notification.tags.created(tag);
      }
    } catch {
      notification.tags.failedToAdd();
    }
  }

  const updateTag = async (updatedTag) => {
    try {
      const tagJson = JSON.stringify(updatedTag);
      const tag = await api.tags.update(updatedTag.id, tagJson);
      if (tag) {
        insertTag(tag);
        notification.tags.updated(tag);
      }
    } catch {
      notification.tags.failedToUpdate();
    }
  }

  const deleteTag = async (tagId) => {
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
    areLoaded: readonly(loaded),
    tagsById: readonly(tagsById),
    loadTags,
    addTag,
    updateTag,
    deleteTag
  }
}