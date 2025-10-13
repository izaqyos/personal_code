import { Controller, Body, Get, Post } from '@nestjs/common';
import { FooService } from './foo.service';
import { FooModel } from './foo.model';

@Controller('foo')
export class FooController {

    constructor(private fooService: FooService) {

    }

    @Get() 
    getAll(): FooModel[] {
        return this.fooService.getAll();
    }

    @Post()
    create(@Body('title') title): FooModel {
        return this.fooService.create(title);
    }
}
