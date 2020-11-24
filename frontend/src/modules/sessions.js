import { ref, reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import useGenerator from "./generator";
import AwaitLock from 'await-lock';

const { setCurrentSession } = useGenerator();

const hasLoaded = ref(false);
const loadSessionsLock = new AwaitLock();

const sessionsById = reactive({});

export default function useSessions() {

    const loadGeneratorSessionsAsync = async () => {
        await loadSessionsLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const sessions = await api.sessions.getAllGenerator();
            if (sessions) {
                sessions.forEach(ses => sessionsById[ses.id] = ses);
                hasLoaded.value = true;
            }
        } catch (e) {
            notification.error("Failed to load generator sessions", e.message);
        } finally {
            loadSessionsLock.release();
        }
    }

    const createGeneratorSessionAsync = async (newSession) => {
        try {
            const sessionJson = JSON.stringify(newSession);
            const session = await api.sessions.createGenerator(sessionJson);
            if (session) {
                sessionsById[session.id] = session;
                setCurrentSession(sessionsById[session.id]);
            }
        } catch (e) {
            notification.error("Failed to create the generator session", e.message);
        }
    }

    return {
        sessionsById: readonly(sessionsById),
        loadGeneratorSessionsAsync,
        createGeneratorSessionAsync,
    }
}