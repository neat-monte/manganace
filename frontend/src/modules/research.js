import { ref, reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import moment from "moment"
import AwaitLock from 'await-lock';

const hasLoaded = ref(false);
const loadLock = new AwaitLock();

const sessionsById = reactive({});

const generalLock = new AwaitLock();

const currentSession = reactive({});

const insertSession = (session) => {
    session.created = moment(session.created).format("YYYY-MM-DD HH:mm");
    sessionsById[session.id] = session;
}

export default function useResearch() {

    const loadResearchSessionsAsync = async () => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded.value) {
                return;
            }
            const sessions = await api.sessions.getAllResearch();
            if (sessions) {
                sessions.forEach(session => insertSession(session));
                hasLoaded.value = true;
            }
        } catch (e) {
            notification.error("Failed to load research sessions", e.message);
        } finally {
            loadLock.release();
        }
    }

    const createResearchSessionAsync = async (newSession) => {
        try {
            const newSessionJson = JSON.stringify(newSession);
            const session = await api.sessions.createResearch(newSessionJson);
            if (session) {
                insertSession(session);
            }
        } catch (e) {
            notification.error("Failed to create the research session", e.message);
        }
    }

    const assignParticipantAsync = async (newParticipant) => {
        await generalLock.acquireAsync();
        try {
            const session = sessionsById[newParticipant.sessionId];
            if (!session || session.participant) {
                notification.warning("Cannot assign participant",
                    "A participant is already assigned to this session");
                return;
            }
            const participantJson = JSON.stringify(newParticipant);
            const participant = await api.research.assignParticipant(participantJson);
            if (participant) {
                session.participant = participant;
                if (currentSession.id === session.id) {
                    currentSession.participant = participant;
                }
            }
        } catch (e) {
            notification.error("Failed to assign the participant", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getTrialsMetaInfoAsync = async () => {
        if (!currentSession) {
            notification.warning("Cannot load trials data", "A session is not selected");
            return;
        }
        await generalLock.acquireAsync();
        try {
            return await api.research.getTrialsMeta(currentSession.id)
        } catch (e) {
            notification.error("Failed to load trials data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getTrialImagesAsync = async (trialMeta) => {
        await generalLock.acquireAsync();
        try {
            const trialMetaJson = JSON.stringify(trialMeta);
            return await api.research.getTrialImages(trialMetaJson)
        } catch (e) {
            notification.error("Failed to load images of the trial", e.message);
        } finally {
            generalLock.release();
        }
    }

    const saveChosenTrialImageAsync = async (chosenImage) => {
        await generalLock.acquireAsync();
        try {
            const imageJson = JSON.stringify(chosenImage);
            const image = await api.images.create(imageJson);
            if (image) {
                currentSession.progress += 1;
                sessionsById[currentSession.id].progress += 1;
            }
        } catch (e) {
            notification.error("Failed to save the answer", e.message);
        } finally {
            generalLock.release();
        }
    }

    const setCurrentSession = (sessionId) => {
        const session = sessionsById[sessionId];
        if (session) {
            Object.assign(currentSession, session)
        }
    }

    const getResultsDataAsync = async () => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getResultsData();
        } catch (e) {
            notification.error("Failed to load results data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getSessionResultsDataAsync = async (sessionId) => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getSessionResultsData(sessionId);
        } catch (e) {
            notification.error("Failed to load results data", e.message);
        } finally {
            generalLock.release();
        }
    }

    const getExportCsvAsync = async () => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getExportCsv();
        } catch (e) {
            notification.error("Failed to export the data", e.message);
        } finally {
            generalLock.release();
        }
    }

    return {
        sessionsLoaded: readonly(hasLoaded),
        sessionsById: readonly(sessionsById),
        currentSession: readonly(currentSession),
        loadResearchSessionsAsync,
        createResearchSessionAsync,
        assignParticipantAsync,
        getTrialsMetaInfoAsync,
        getTrialImagesAsync,
        getResultsDataAsync,
        getSessionResultsDataAsync,
        getExportCsvAsync,
        saveChosenTrialImageAsync,
        setCurrentSession,
    }
}