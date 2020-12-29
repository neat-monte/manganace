import { ref, reactive, readonly } from 'vue'
import api from '@/services/api'
import notification from "@/services/notification"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const generalLock = new AwaitLock();

const sessionsById = reactive({});

const currentSession = reactive({});

export default function useGeneratorSessions() {

    const loadGeneratorSessionsAsync = async () => {
        await generalLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const sessions = await api.sessions.getAllGenerator();
            sessions.forEach(ses => sessionsById[ses.id] = ses);
            hasLoaded.value = true;
        } catch (e) {
            notification.error("Failed to load generator sessions", e.message);
        } finally {
            generalLock.release();
        }
    }

    const createGeneratorSessionAsync = async (newSession) => {
        await generalLock.acquireAsync();
        try {
            const sessionJson = JSON.stringify(newSession);
            const session = await api.sessions.createGenerator(sessionJson);
            sessionsById[session.id] = session;
            setCurrentSession(sessionsById[session.id]);
        } catch (e) {
            notification.error("Failed to create the generator session", e.message);
        } finally {
            generalLock.release();
        }
    }

    const deleteGeneratorSessionAsync = async (sessionId) => {
        await generalLock.acquireAsync();
        try {
            await api.sessions.destroyGenerator(sessionId);
            delete sessionsById[sessionId];
            setCurrentSession(null);
        } catch (e) {
            notification.error("Failed to delete the generator session", e.message);
        } finally {
            generalLock.release();
        }
    }

    const setCurrentSession = (session) => {
        if (session && session.id && session.name) {
            currentSession.id = session.id;
            currentSession.name = session.name;
        } else if (session === null) {
            Object.keys(currentSession).forEach(k => currentSession[k] = undefined);
        }
    }

    return {
        sessionsById: readonly(sessionsById),
        currentSession: readonly(currentSession),
        loadGeneratorSessionsAsync,
        createGeneratorSessionAsync,
        deleteGeneratorSessionAsync,
        setCurrentSession
    }
}