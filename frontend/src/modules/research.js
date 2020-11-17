import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadLock = new AwaitLock();

const sessionsById = reactive({});

const insertSession = (session) => {
    sessionsById[session.id] = session;
}

export default function useResearch() {

    const loadSessionsAsync = async () => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const sessions = await api.research.getSessions();
            if (sessions) {
                sessions.forEach(session => insertSession(session));
                hasLoaded.value = true;
            }
        } catch {
            notification.sessions.failedToLoad();
        } finally {
            loadLock.release();
        }
    }

    const addSessionAsync = async (newSession) => {
        try {
            const newSessionJson = JSON.stringify(newSession);
            const session = await api.research.initializeSession(newSessionJson);
            if (session) {
                insertSession(session);
                notification.sessions.created(session);
            }
        } catch {
            notification.sessions.failedToAdd();
        }
    }

    return {
        sessionsLoaded: readonly(hasLoaded),
        sessionsById: readonly(sessionsById),
        loadSessionsAsync,
        addSessionAsync
    }
}