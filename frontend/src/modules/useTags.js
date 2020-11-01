import { ref, reactive, readonly } from 'vue'
import http from '@/services/http'

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
    const tags = await http.tags.getAll();
    if (tags) {
      tags.forEach(tag => insertTag(tag));
    }
  }

  const addTag = async (newTag) => {
    const tagJson = JSON.stringify(newTag);
    console.log(tagJson);
    const tag = await http.tags.create(tagJson);
    if (tag) {
      insertTag(tag);
      return state.tagsById[tag.id];
    }
  }

  return {
    areLoaded: readonly(loaded),
    tagsById: readonly(state.tagsById),
    loadTags,
    addTag
  }
}