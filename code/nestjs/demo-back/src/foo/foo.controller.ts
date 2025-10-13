import { Controller, Get, Body, Post, Param, Delete, Patch, UsePipes, ValidationPipe } from '@nestjs/common';
import { FooService } from './foo.service';
import { FooModel, FooState } from './foo.model';
import { FooDTO } from './dto/foo.dto';

@Controller('foo')
export class FooController {

    constructor(private fooService: FooService) {

    }

    @Delete(':id')
    deleteById(@Param('id') id: string): void {
        this.fooService.deleteById(id); 
    }

    @Get(':id')
    getById(@Param('id') id: string): FooModel {
        return this.fooService.getById(id); 
    }

    @Get()
    getAll(): FooModel[] {
        return this.fooService.getAll(); 
    }

    @Post()
    @UsePipes(ValidationPipe)
    createFoo(@Body() fooDTO: FooDTO): FooModel {
        return this.fooService.createFoo(fooDTO);
    }

    @Patch(':id/state')
    update(@Param('id') id: string, @Body('state') state: FooState): FooModel {
        return this.fooService.update(id, state);
    }
}
