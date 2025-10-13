import { Body, Controller, Delete, Get, Param, Patch, Post, UsePipes, ValidationPipe } from '@nestjs/common';
import { CreateFooDTO } from './dto/create-foo.dto';
import { Foo, FooState } from './foo.model';
import { FooService } from './foo.service';

@Controller('foo')
export class FooController {
    constructor(private fooService: FooService) {

    }

    @Get()
    getFoos(): Foo[] {
        return this.fooService.getFoos();
    }

    @Get(':id')
    getById(@Param('id') id: string): Foo {
        return this.fooService.getById(id);
    }

    @Delete(':id')
    delById(@Param('id') id: string): void {
        this.fooService.delById(id);
    }

    @Patch(':id/state')
    updateState(@Param('id') id: string, @Body('state') state: FooState): Foo {
        console.log('got request to update state of %s to %s', id, state);
        return this.fooService.updateState(id, state);
    }


    @Post()
    @UsePipes(ValidationPipe)
    createFoo(@Body() createFooDto: CreateFooDTO) {
        return this.fooService.createFoo(createFooDto);
    }
}
