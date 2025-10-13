export interface FooModel {
    id: string;
    title: string;
    state: FooState; 
}

export enum FooState {
    INIT = 'INIT',
    WIP = 'WIP',
    DONE = 'DONE',
}