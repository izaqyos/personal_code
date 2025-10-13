import { Injectable } from '@nestjs/common';
import { FooModel, FooState } from './foo.model';
import {v1 as uuidv1  } from "uuid";
import { FooDTO } from './dto/foo.dto';

@Injectable()
export class FooService {
    private foos: FooModel[] = [];

    getAll(): FooModel[] {
        return this.foos;
    }

    createFoo(fooDTO: FooDTO) {
        const {title} = fooDTO;
        const foo = {
            id: uuidv1(),
            title,
            state: FooState.INIT
        };
        this.foos.push(foo);
        return foo;
    }

    getById(id: string): FooModel {
        return this.foos.find(elem => elem.id === id);
    }

    deleteById(id: string): void {
        const index = this.foos.findIndex(elem => elem.id === id);
        if (index > -1) {
            this.foos.splice(index, 1);
        }
    }

    update(id: string, state: FooState): FooModel {
        const foo = this.getById(id);
        foo.state = state;
        return foo;
    }
}
