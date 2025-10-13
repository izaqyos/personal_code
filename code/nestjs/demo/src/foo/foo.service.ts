import { Get, Injectable } from '@nestjs/common';
import { FooModel, FooState } from './foo.model';
import {v1 as uuidv1} from 'uuid';

@Injectable()
export class FooService {
    private foos: FooModel[] = [];

    getAll(): FooModel[]  {
        return this.foos;
    }

    create(title: string): FooModel {
        const foo: FooModel = {
            id: uuidv1(),
            title,
            state: FooState.INIT, 
        };

        this.foos.push(foo);
        return foo;
    }
}
