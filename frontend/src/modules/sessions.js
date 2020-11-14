import { ref, reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadSessionsLock = new AwaitLock();

const sessionsById = reactive({});

const insertSession = (session) => {
    sessionsById[session.id] = session;
}

export default function useSessions() {

    const loadSessionsAsync = async () => {
        await loadSessionsLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const sessions = await api.sessions.getAll();
            if (sessions) {
                sessions.forEach(session => insertSession(session));
                hasLoaded.value = true;
            }
        } catch {
            notification.sessions.failedToLoad();
        } finally {
            loadSessionsLock.release();
        }
    }

    const addSessionAsync = async (newSession) => {
        try {
            const sessionJson = JSON.stringify(newSession);
            const session = await api.sessions.create(sessionJson);
            if (session) {
                insertSession(session);
                notification.sessions.created(session);
            }
        } catch {
            notification.sessions.failedToAdd();
        }
    }

    const updateSessionAsync = async (updatedSession) => {
        try {
            const sessionJson = JSON.stringify(updatedSession);
            const session = await api.sessions.update(updatedSession.id, sessionJson);
            if (session) {
                insertSession(session);
                notification.sessions.updated(session);
            }
        } catch {
            notification.sessions.failedToUpdate();
        }
    }

    const deleteSessionAsync = async (sessionId) => {
        try {
            const session = await api.sessions.destroy(sessionId);
            if (session) {
                delete insertSession[session.id];
                notification.sessions.deleted(session);
            }
        } catch {
            notification.sessions.failedToDelete();
        }
    }

    return {
        areLoaded: readonly(hasLoaded),
        sessionsById: readonly(sessionsById),
        loadSessionsAsync,
        addSessionAsync,
        updateSessionAsync,
        deleteSessionAsync
    }
}