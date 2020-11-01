import { ref, reactive, readonly } from "vue"
import moment from "moment"
import http from "@/services/http"
import notification from "@/services/notification"

const loaded = ref(false);

const state = reactive({
  collectionsById: {}
});

function insertCollection(collection) {
  collection.created = moment(collection.created).format("YYYY-MM-DD HH:mm");
  collection.updated = collection.updated !== null ? moment(collection.updated).format("YYYY-MM-DD HH:mm") : null;
  state.collectionsById[collection.id] = collection;
}

export default function useCollections() {
  const loadCollections = async () => {
    try {
      if (state !== undefined && loaded.value) {
        return;
      }
      const collections = await http.collections.getAllWithoutRelations();
      collections.forEach(collection => insertCollection(collection));
      loaded.value = true;
    } catch {
      notification.collections.failedToLoad();
    }
  }

  const addCollection = async (newCollection) => {
    try {
      const collectionJson = JSON.stringify(newCollection);
      const collection = await http.collections.create(collectionJson);
      if (collection) {
        insertCollection(collection);
        notification.collections.created(collection);
      }
    } catch {
      notification.collections.failedToAdd();
    }
  }

  const updateCollection = async (updatedCollection) => {
    try {
      const collectionJson = JSON.stringify(updatedCollection);
      const collection = await http.collections.update(updatedCollection.id, collectionJson);
      if (collection) {
        insertCollection(collection);
        notification.collections.updated(collection);
      }
    } catch {
      notification.collections.failedToUpdate();
    }
  }

  const deleteCollection = async (collectionId) => {
    try {
      const collection = await http.collections.destroy(collectionId);
      if (collection) {
        delete state.collectionsById[collection.id];
        notification.collections.deleted(collection);
      }
    } catch {
      notification.collections.failedToDelete();
    }
  }

  return {
    collectionsLoaded: readonly(loaded),
    collectionsById: readonly(state.collectionsById),
    loadCollections,
    addCollection,
    updateCollection,
    deleteCollection
  }
}