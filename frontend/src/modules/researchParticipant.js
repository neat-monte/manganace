import api from "@/services/api"
import notification from "@/services/notification"
import useResearchSessions from "./researchSessions";
import AwaitLock from 'await-lock';

const { sessionsBySettingId, updateParticipant, removeParticipant } = useResearchSessions();

const generalLock = new AwaitLock();

export default function useResearchParticipant() {

    const assignParticipantAsync = async (researchSettingId, newParticipant) => {
        await generalLock.acquireAsync();
        try {
            const session = sessionsBySettingId[researchSettingId].filter(s => s.id === newParticipant.sessionId)[0];
            if (!session || session.participant) {
                notification.warning("Cannot assign participant",
                    "A participant is already assigned to this session");
                return;
            }
            const participantJson = JSON.stringify(newParticipant);
            const participant = await api.research.assignParticipant(participantJson);
            updateParticipant(researchSettingId, participant);
        } catch (e) {
            notification.error("Failed to assign the participant", e.message);
        } finally {
            generalLock.release();
        }
    }

    const deleteParticipantAsync = async (researchSettingId, participantId) => {
        await generalLock.acquireAsync();
        try {
            const participant = await api.research.destroyParticipant(participantId);
            removeParticipant(researchSettingId, participant);
        } catch (e) {
            notification.error("Failed to delete the participant", e.message);
        } finally {
            generalLock.release();
        }
    }

    return {
        assignParticipantAsync,
        deleteParticipantAsync,
    }
}