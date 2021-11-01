import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate, IMsg, WithTaskId, ITaskPayload } from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

const apiPrefix = apiUrl + '/api/v1';

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiPrefix}/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiPrefix}/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiPrefix}/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiPrefix}/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiPrefix}/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiPrefix}/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiPrefix}/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiPrefix}/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async queueTask(taskParam: IMsg) {
    return axios.post<IMsg & WithTaskId>(`${apiPrefix}/utils/queue-celery-task/`, taskParam);
  },
  async getTaskStatus(taskId: string) {
    return axios.get<ITaskPayload>(`${apiPrefix}/utils/task-status/${taskId}`);
  },
};
