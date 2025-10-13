export interface Foo {
    id: string;
    title: string;
    state: FooState;
}

export enum FooState {
    Init = 'Init',
    WIP = 'WIP',
    Done = 'Done',
}