import { reactive, readonly } from "vue"
import moment from "moment"
import http from "@/services/http"

const state = reactive({
  collections: {}
});

function insertCollectionObject(collection) {
  collection.created = moment(collection.created).format("YYYY-MM-DD HH:mm");
  collection.updated = collection.updated !== null ? moment(collection.updated).format("YYYY-MM-DD HH:mm") : null;
  state.collections[collection.id] = collection;
}

export default function useCollections() {
  const loadCollections = async () => {
    const collections = await http.collections.getAllWithoutRelations();
    collections.forEach(collection => insertCollectionObject(collection));
  }

  const addCollection = async (newCollection) => {
    const collectionJson = JSON.stringify(newCollection);
    const collection = await http.collections.create(collectionJson);
    if (collection) {
      insertCollectionObject(collection);
      return state.collections[collection.id]
    }
  }

  const updateCollection = async (updatedCollection) => {
    const collectionJson = JSON.stringify(updatedCollection);
    const collection = await http.collections.update(updatedCollection.id, collectionJson);
    if (collection) {
      insertCollectionObject(collection);
      return state.collections[collection.id]
    }
  }

  const deleteCollection = async (collectionId) => {
    const collection = await http.collections.destroy(collectionId);
    if (collection) {
      const deleted = state.collections[collection.id];
      delete state.collections[collection.id];
      return deleted;
    }
  }

  return {
    state: readonly(state),
    loadCollections,
    addCollection,
    updateCollection,
    deleteCollection
  }
}