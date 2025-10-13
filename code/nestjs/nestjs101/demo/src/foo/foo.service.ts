import { Injectable } from '@nestjs/common';
import { Foo, FooState } from './foo.model';
import {v1 as uuidv1} from 'uuid';
import { CreateFooDTO } from './dto/create-foo.dto';
@Injectable()
export class FooService {

    private foos: Foo[] = [];

    getFoos(): Foo[] {
        return this.foos; 
    }

    getById(id: string): Foo{
        return this.foos.find(elem => elem.id === id); 
    }

    updateState(id: string, state: FooState): Foo{
        const foo = this.getById(id);
        foo.state = state; 
        return foo
    }

    delById(id: string): void{
        const index = this.foos.findIndex(elem => elem.id === id); 
        if (index > -1) {
            this.foos.splice(index, 1); 
        } 
    }

    createFoo(createFooDTO: CreateFooDTO): Foo {
        const {title} = createFooDTO;
        const aFoo: Foo = {
            id: uuidv1(),
            title,
            state: FooState.Init,
        };
        
        this.foos.push(aFoo);
        return aFoo;
    }
}
