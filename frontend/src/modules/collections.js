import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import moment from "moment"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadLock = new AwaitLock();

const collectionsById = reactive({});

const insertCollection = (collection) => {
    collection.created = moment(collection.created).format("YYYY-MM-DD HH:mm");
    collection.updated = collection.updated !== null ? moment(collection.updated).format("YYYY-MM-DD HH:mm") : null;
    collectionsById[collection.id] = collection;
}

export default function useCollections() {

    const loadCollectionsAsync = async () => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const collections = await api.collections.getAllUser();
            collections.forEach(collection => insertCollection(collection));
            hasLoaded.value = true;
        } catch (e) {
            notification.error("Failed to load collections", e.message)
        } finally {
            loadLock.release();
        }
    }

    const createCollectionAsync = async (newCollection) => {
        try {
            const collectionJson = JSON.stringify(newCollection);
            const collection = await api.collections.createUser(collectionJson);
            if (collection) {
                insertCollection(collection);
            }
        } catch (e) {
            notification.error("Failed to create the collection", e.message);
        }
    }

    const updateCollectionAsync = async (updatedCollection) => {
        try {
            const collectionJson = JSON.stringify(updatedCollection);
            const collection = await api.collections.updateUser(updatedCollection.id, collectionJson);
            if (collection) {
                insertCollection(collection);
            }
        } catch (e) {
            notification.error("Failed to update the collection", e.message);
        }
    }

    const deleteCollectionAsync = async (collectionId) => {
        try {
            const collection = await api.collections.destroyUser(collectionId);
            if (collection) {
                delete collectionsById[collection.id];
            }
        } catch (e) {
            notification.error("Failed to delete the collection", e.message)
        }
    }

    return {
        collectionsById: readonly(collectionsById),
        loadCollectionsAsync,
        createCollectionAsync,
        updateCollectionAsync,
        deleteCollectionAsync
    }
}