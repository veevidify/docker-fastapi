import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IUserProfileCreate, IUserProfileUpdate } from '@/interfaces';
import { State } from '../state';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import {
  commitSetUsers,
  commitSetUser,
  commitUpdateTaskId,
  commitSetCurrentTask,
  commitUpdateTaskResult,
} from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import {
    commitAddNotification,
    commitRemoveNotification,
} from '../main/mutations';
import { IMsg, WithTaskId } from '@/interfaces';

type MainContext = ActionContext<AdminState, State>;

export const actions = {
    async actionGetUsers(context: MainContext) {
        try {
            const response = await api.getUsers(context.rootState.main.token);
            if (response) {
                commitSetUsers(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUser(context: MainContext, payload: { id: number, user: IUserProfileUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateUser(context.rootState.main.token, payload.id, payload.user),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createUser(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    // send to enqueue the task, receive id, update state
    async actionSendTaskForQueue(context: MainContext, payload: IMsg) {
        commitSetCurrentTask(context, payload);
        const authToken = context.rootState.main.token;
        try {
            const taskHandle = await api.queueTask(payload, authToken);
            const data = taskHandle.data;
            commitUpdateTaskId(context, data);
        } catch (e) {
            const err = { msg: e, task_id: e };
            commitUpdateTaskId(context, err);
        }
    },
    // using state's current task id to poll result
    async actionPollTaskResult(context: MainContext, payload: WithTaskId) {
        const currentTaskMsg = context.state.currentTask.msg;
        const currentTaskId = context.state.taskResult?.task_id || '';

        const authToken = context.rootState.main.token;
        if (! currentTaskId) {
            const err = { msg: 'No task_id' , task_id: currentTaskId };
            commitUpdateTaskId(context, err);
        } else {
            try {
                const resultData = await api.getTaskStatus(currentTaskId, authToken);
                const { data } = resultData;

                commitUpdateTaskResult(context, data);
            } catch (e) {
                const err = {
                    task_id: currentTaskId,
                    task_result: e,
                    task_status: 'failed',
                };
                commitUpdateTaskResult(context, err);
            }
        }
    },
    // remove current task's info to refresh the view
    async actionClearCurrentTask(context: MainContext) {
        commitSetCurrentTask(context, { msg: '' });
        commitUpdateTaskResult(context, null);
    },
};

const { dispatch } = getStoreAccessors<AdminState, State>('');

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchQueueTask = dispatch(actions.actionSendTaskForQueue);
export const dispatchPollTaskResult = dispatch(actions.actionPollTaskResult);
export const dispatchClearTask = dispatch(actions.actionClearCurrentTask);
