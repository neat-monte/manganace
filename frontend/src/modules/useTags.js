import { ref, reactive, readonly } from 'vue'
import http from '@/services/http'
import notification from "@/services/notification"

const loaded = ref(false);

const state = reactive({
  tagsById: {}
});

function insertTag(tag) {
  state.tagsById[tag.id] = tag;
}

export default function useTags() {

  const loadTags = async () => {
    if (state !== undefined && loaded.value) {
      return;
    }
    try {
      const tags = await http.tags.getAll();
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
      const tag = await http.tags.create(tagJson);
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
      const tag = await http.tags.update(updatedTag.id, tagJson);
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
      const tag = await http.tags.destroy(tagId);
      if (tag) {
        delete state.tagsById[tag.id];
        notification.tags.deleted(tag);
      }
    } catch {
      notification.tags.failedToDelete();
    }
  }

  return {
    areLoaded: readonly(loaded),
    tagsById: readonly(state.tagsById),
    loadTags,
    addTag,
    updateTag,
    deleteTag
  }
}