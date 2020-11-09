import { ref, reactive, readonly } from "vue"
import moment from "moment"
import api from "@/services/api"
import notification from "@/services/notification"

const loaded = ref(false);
const collectionsById = reactive({});

function insertCollection(collection) {
  collection.created = moment(collection.created).format("YYYY-MM-DD HH:mm");
  collection.updated = collection.updated !== null ? moment(collection.updated).format("YYYY-MM-DD HH:mm") : null;
  collectionsById[collection.id] = collection;
}

export default function useCollections() {

  const loadCollections = async () => {
    try {
      if (collectionsById !== undefined && loaded.value) {
        return;
      }
      const collections = await api.collections.getAll();
      collections.forEach(collection => insertCollection(collection));
      loaded.value = true;
    } catch {
      notification.collections.failedToLoad();
    }
  }

  const addCollection = async (newCollection) => {
    try {
      const collectionJson = JSON.stringify(newCollection);
      const collection = await api.collections.create(collectionJson);
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
      const collection = await api.collections.update(updatedCollection.id, collectionJson);
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
      const collection = await api.collections.destroy(collectionId);
      if (collection) {
        delete collectionsById[collection.id];
        notification.collections.deleted(collection);
      }
    } catch {
      notification.collections.failedToDelete();
    }
  }

  return {
    collectionsLoaded: readonly(loaded),
    collectionsById: readonly(collectionsById),
    loadCollections,
    addCollection,
    updateCollection,
    deleteCollection
  }
}