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

    const loadSessionsAsync = async () => {
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
        } catch {
            notification.sessions.failedToLoad();
        } finally {
            loadLock.release();
        }
    }

    const addSessionAsync = async (newSession) => {
        try {
            const newSessionJson = JSON.stringify(newSession);
            const session = await api.sessions.createResearch(newSessionJson);
            if (session) {
                insertSession(session);
                notification.sessions.created(session);
            }
        } catch {
            notification.sessions.failedToAdd();
        }
    }

    const assignParticipantAsync = async (newParticipant) => {
        await generalLock.acquireAsync();
        try {
            const session = sessionsById[newParticipant.sessionId];
            if (!session || session.participant) {
                notification.sessions.cannotAssignParticipant();
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
        } catch {
            notification.sessions.failedToAssignParticipant()
        } finally {
            generalLock.release();
        }
    }

    const getTrialsMetaInfoAsync = async () => {
        if (!currentSession) {
            notification.research.cannotLoadTrialsMetaInfo();
            return;
        }
        await generalLock.acquireAsync();
        try {
            return await api.research.getTrialsMeta(currentSession.id)
        } catch {
            notification.research.failedToLoadTrialsMetaInfo();
        } finally {
            generalLock.release();
        }
    }

    const getTrialImagesAsync = async (trialMeta) => {
        await generalLock.acquireAsync();
        try {
            const trialMetaJson = JSON.stringify(trialMeta);
            return await api.research.getTrialImages(trialMetaJson)
        } catch {
            notification.research.failedToLoadTrialImages();
        } finally {
            generalLock.release();
        }
    }

    const saveChosenTrialImage = async (chosenImage) => {
        await generalLock.acquireAsync();
        try {
            const imageJson = JSON.stringify(chosenImage);
            const image = await api.images.create(imageJson);
            if (image) {
                currentSession.progress += 1;
                sessionsById[currentSession.id].progress += 1;
            }
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
        } finally {
            generalLock.release();
        }
    }

    const getExportCsvAsync = async () => {
        await generalLock.acquireAsync()
        try {
            return await api.research.getExportCsv();
        } finally {
            generalLock.release();
        }
    }

    return {
        sessionsLoaded: readonly(hasLoaded),
        sessionsById: readonly(sessionsById),
        currentSession: readonly(currentSession),
        loadSessionsAsync,
        addSessionAsync,
        assignParticipantAsync,
        setCurrentSession,
        getTrialsMetaInfoAsync,
        getTrialImagesAsync,
        saveChosenTrialImage,
        getResultsDataAsync,
        getExportCsvAsync
    }
}