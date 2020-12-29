import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const gendersLoaded = ref(false);
const gendersLoadLock = new AwaitLock();

const gendersById = reactive({});

export default function useExtras() {

    const loadGendersAsync = async () => {
        await gendersLoadLock.acquireAsync();
        try {
            if (gendersLoaded.value) {
                return;
            }
            const genders = await api.extras.getGendersOptions();
            genders.forEach(gen => gendersById[gen.id] = gen);
            gendersLoaded.value = true;
        } catch (e) {
            notification.error("Failed to load genders", e.message);
        } finally {
            gendersLoadLock.release();
        }
    }

    return {
        gendersById: readonly(gendersById),
        loadGendersAsync,
    }
}