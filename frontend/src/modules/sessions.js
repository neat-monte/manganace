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

    const loadSessionsAsync = async () => {
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
        } catch {
            notification.sessions.failedToLoad();
        } finally {
            loadSessionsLock.release();
        }
    }

    const addSessionAsync = async (newSession) => {
        try {
            const sessionJson = JSON.stringify(newSession);
            const session = await api.sessions.createGenerator(sessionJson);
            if (session) {
                sessionsById[session.id] = session;
                notification.sessions.created(session);
                setCurrentSession(sessionsById[session.id])
            }
        } catch {
            notification.sessions.failedToAdd();
        }
    }

    const updateSessionAsync = async (updatedSession) => {
        try {
            const sessionJson = JSON.stringify(updatedSession);
            const session = await api.sessions.updateGenerator(updatedSession.id, sessionJson);
            if (session) {
                sessionsById[session.id] = session;
                notification.sessions.updated(session);
            }
        } catch {
            notification.sessions.failedToUpdate();
        }
    }

    const deleteSessionAsync = async (sessionId) => {
        try {
            const session = await api.sessions.destroyGenerator(sessionId);
            if (session) {
                delete sessionsById[session.id];
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