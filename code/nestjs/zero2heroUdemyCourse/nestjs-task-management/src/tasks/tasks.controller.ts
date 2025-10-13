import { Controller, Patch, Get, Post, Delete, Body, Param, Query, UsePipes, ValidationPipe, ParseIntPipe } from '@nestjs/common';
import { TasksService } from './tasks.service';
//import { Task, TasksStatus } from './tasks.model'; //unused post typeOrm
import { CreateTaskDto } from './dto/create-task.dto';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { TaskStatusValidationPipe } from './pipes/task-status-validation.pipe';
import { Task } from './task.entity';

@Controller('tasks')
export class TasksController {
    constructor(private tasksService: TasksService) {}

    // @Get()
    // getTasks(@Query(ValidationPipe) filterDto: GetTasksFilterDto): Task[] {
    //     console.log('getTasks filterDto ', filterDto);

    //     //destruct
    //     //const {status, search}  = filterDto;
    //     //if (!status && !search){
    //     //    return this.tasksService.getAllTasks();
    //     //}
    //     //else{
    //     //    return this.tasksService.getTasksWithFilter(filterDto);
    //     //}

    //     //use Objeck.keys()
    //     if (Object.keys(filterDto).length) {
    //         return this.tasksService.getTasksWithFilter(filterDto);
    //     } else {
    //         return this.tasksService.getAllTasks();
    //     }
    //     
    // }


     @Get('/:id')
     getTaskById(@Param('id', ParseIntPipe) id: number): Promise<Task> {
         return this.tasksService.getTaskById(id);
     }

    // @Get('/:id')
    // getTaskById(@Param('id') id: string) {
    //     return this.tasksService.getTaskById(id);
    // }

    // @Delete('/:id')
    // deleteTaskById(@Param('id') id: string) {
    //     return this.tasksService.deleteTaskById(id);
    // }

    // @Patch('/:id/status')
    // patchTaskStatus(
    //     @Param('id') id: string,
    //     @Body('status', TaskStatusValidationPipe) status: TasksStatus,
    // ): Task {
    //     return this.tasksService.updateTaskStatus(id, status);
    // }


    // ////Get all body
    // //@Post()
    // //createTask(@Body() body) {
    // //    console.log('body', body);
    // //}


    // ////get selectively
    // //@Post()
    // //createTask(
    // //    @Body('title') title: string,
    // //    @Body('description') description: string,
    // //    ): Task {
    // //    console.log('title', title);
    // //    console.log('description', description);
    // //    return this.tasksService.createTask(title, description);
    // //}

    // //use DTO
    // @Post()
    // @UsePipes(ValidationPipe)
    // createTask(
    //     @Body() createTaskDto: CreateTaskDto,
    //     ): Task {
    //     console.log('createTaskDto', createTaskDto);
    //     return this.tasksService.createTask(createTaskDto);
    // }

}
