import { IUserProfile, IMsg, ITaskPayload } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    currentTask: IMsg;
    taskResult: ITaskPayload | null;
}
