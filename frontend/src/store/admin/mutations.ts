import { IUserProfile, ITaskPayload, IMsg, WithTaskId } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setCurrentTask(state: AdminState, payload: IMsg) {
        state.currentTask = payload;
    },
    updateTaskId(state: AdminState, payload: IMsg & WithTaskId) {
        state.taskResult = {
            task_id: payload.task_id,
            task_status: 'pending',
            task_result: 'pending',
        };
    },
    updateTaskResult(state: AdminState, payload: ITaskPayload | null) {
        state.taskResult = payload;
    },
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
export const commitSetCurrentTask = commit(mutations.setCurrentTask);
export const commitUpdateTaskId = commit(mutations.updateTaskId);
export const commitUpdateTaskResult = commit(mutations.updateTaskResult);
