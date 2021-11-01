export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IMsg {
    msg: string;
}

export interface WithTaskId {
    task_id: string;
}

export interface ITaskStatus {
    task_status: string;
    task_result: string;
}

export type ITaskPayload = ITaskStatus & WithTaskId;
