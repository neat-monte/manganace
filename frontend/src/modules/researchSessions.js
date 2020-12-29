import { reactive, readonly } from "vue"
import api from "@/services/api"
import notification from "@/services/notification"
import useGenerator from "./generator";
import moment from "moment"
import AwaitLock from 'await-lock';

const { usingGeneratorAsync, finishedUsingGenerator } = useGenerator();

const hasLoaded = reactive({});
const loadLock = new AwaitLock();

const sessionsBySettingId = reactive({});

const currentSession = reactive({});

const researchGenerateRequest = reactive({});

export default function useResearchSessions() {

    const insertResearchSession = (session) => {
        session.created = moment(session.created).format("DD-MM-YYYY HH:mm");
        if (!sessionsBySettingId[session.researchSettingId]) {
            sessionsBySettingId[session.researchSettingId] = [];
        }
        sessionsBySettingId[session.researchSettingId].push(session);
    }

    const loadResearchSessionsAsync = async (settingId) => {
        await loadLock.acquireAsync();
        try {
            if (hasLoaded[settingId]) {
                return;
            }
            const sessions = await api.sessions.getAllResearch(settingId);
            if (!sessionsBySettingId[settingId]) {
                sessionsBySettingId[settingId] = [];
            }
            sessions.forEach(session => insertResearchSession(session));
            hasLoaded[settingId] = true;
        } catch (e) {
            notification.error("Failed to load research sessions", e.message);
        } finally {
            loadLock.release();
        }
    }

    const createResearchSessionsAsync = async (newSession, count) => {
        researchGenerateRequest.done = 1;
        researchGenerateRequest.total = count;
        researchGenerateRequest.inProgress = true;

        const newSessionJson = JSON.stringify(newSession);
        for (let i = count; i > 0; i--) {
            await usingGeneratorAsync();
            try {
                const session = await api.sessions.createResearch(newSessionJson);
                insertResearchSession(session);
                researchGenerateRequest.done += 1;

            } catch (e) {
                notification.error("Failed to generate the research session", e.message);
            } finally {
                finishedUsingGenerator();
            }
        }
        researchGenerateRequest.inProgress = false;
    }

    const deleteResearchSessionAsync = async (sessionId) => {
        await loadLock.acquireAsync();
        try {
            const session = await api.sessions.destroyResearch(sessionId);
            const index = sessionsBySettingId[session.researchSettingId].indexOf(session);
            sessionsBySettingId[session.researchSettingId].splice(index, 1);
        } catch (e) {
            notification.error("Failed to delete research session", e.message);
        } finally {
            loadLock.release();
        }
    }

    const setCurrentSession = (settingId, sessionId) => {
        const session = sessionsBySettingId[settingId].filter(s => s.id === sessionId)[0];
        if (session) {
            Object.assign(currentSession, session)
        }
    }

    const updateParticipant = (settingId, participant) => {
        const session = sessionsBySettingId[settingId].filter(s => s.id === participant.sessionId)[0];
        session.participant = participant;
        if (currentSession.id === session.id) {
            currentSession.participant = participant;
        }
    }

    const removeParticipant = (settingId, participant) => {
        const session = sessionsBySettingId[settingId].filter(s => s.id === participant.sessionId)[0];
        session.participant = null;
        if (currentSession.id === session.id) {
            currentSession.participant = null;
        }
        session.progress = 0;
    }

    const incrementProgress = () => {
        if (!currentSession) {
            return;
        }
        currentSession.progress++;
        sessionsBySettingId[currentSession.researchSettingId].filter(s => s.id === currentSession.id)[0].progress++;
    }

    return {
        sessionsBySettingId: readonly(sessionsBySettingId),
        sessionsLoadStatus: readonly(hasLoaded),
        currentSession: readonly(currentSession),
        researchGenerateRequest: readonly(researchGenerateRequest),
        loadResearchSessionsAsync,
        createResearchSessionsAsync,
        deleteResearchSessionAsync,
        setCurrentSession,
        insertResearchSession,
        updateParticipant,
        removeParticipant,
        incrementProgress,
    }
}