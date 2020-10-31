import { reactive, readonly } from "vue"
import moment from "moment"
import http from "@/services/http"

const state = reactive({
  loaded: false,
  collectionsById: {}
});

function insertCollection(collection) {
  collection.created = moment(collection.created).format("YYYY-MM-DD HH:mm");
  collection.updated = collection.updated !== null ? moment(collection.updated).format("YYYY-MM-DD HH:mm") : null;
  state.collectionsById[collection.id] = collection;
}

export default function useCollections() {
  const loadCollections = async () => {
    if (state !== undefined && state.loaded) {
      return;
    }
    const collections = await http.collections.getAllWithoutRelations();
    collections.forEach(collection => insertCollection(collection));
    state.loaded = true;
  }

  const addCollection = async (newCollection) => {
    const collectionJson = JSON.stringify(newCollection);
    const collection = await http.collections.create(collectionJson);
    if (collection) {
      insertCollection(collection);
      return state.collectionsById[collection.id];
    }
  }

  const updateCollection = async (updatedCollection) => {
    const collectionJson = JSON.stringify(updatedCollection);
    const collection = await http.collections.update(updatedCollection.id, collectionJson);
    if (collection) {
      insertCollection(collection);
      return state.collectionsById[collection.id];
    }
  }

  const deleteCollection = async (collectionId) => {
    const collection = await http.collections.destroy(collectionId);
    if (collection) {
      const deleted = state.collectionsById[collection.id];
      delete state.collectionsById[collection.id];
      return deleted;
    }
  }

  return {
    collectionsById: readonly(state.collectionsById),
    loadCollections,
    addCollection,
    updateCollection,
    deleteCollection
  }
}