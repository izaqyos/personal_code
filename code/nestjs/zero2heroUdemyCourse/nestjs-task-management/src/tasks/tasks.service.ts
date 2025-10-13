import { Injectable, NotFoundException } from '@nestjs/common';
// import { Task, TasksStatus } from './tasks.model';
// import * as uuid from 'uuid/v1'; //only required pre DB connection. @PrimaryGeneratedColumn() decorated id is auto generated

import { CreateTaskDto } from './dto/create-task.dto';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { TaskRepository } from './task.repository';
import { InjectRepository } from '@nestjs/typeorm';
import { Task } from './task.entity';

@Injectable()
export class TasksService {
    constructor(
        @InjectRepository(TaskRepository)
        private taskRepository: TaskRepository,
    ) {}
    // //private tasks: Task[] = []; //pre DB impl

    // getAllTasks(): Task[]  {
    //     return this.tasks;
    // }

    // getTasksWithFilter(filterDto: GetTasksFilterDto): Task[]  {
    //     const {status, search} = filterDto;

    //     let tasks = this.getAllTasks();

    //     if (status) {
    //         tasks = tasks.filter(elem => elem.status === status);
    //     }
    //     if (search) {
    //         tasks = tasks.filter(elem =>
    //             elem.title.includes(search) ||
    //             elem.description.includes(search),
    //             );
    //     }
    //     return tasks;
    // }

    async getTaskById(id: number): Promise<Task> {
        const task =  await this.taskRepository.findOne(id);
        if (!task) {
             throw new NotFoundException(`task ${id} not found! `);
         }

        return task;
    }

    // getTaskById(id: string): Task{
    //     let task =  this.tasks.find( task => task.id  === id );
    //     if (task) {
    //         return this.tasks.find( task => task.id  === id );
    //     }
    //     else {
    //         throw new NotFoundException(`task ${id} not found! `);
    //     }
    // }

    // deleteTaskById(id: string): Task[] {
    //     let task = this.getTaskById(id); //throw NotFound not exist
    //     this.tasks = this.tasks.filter(elem => elem.id !== id); //so this line only when found...
    //     return this.tasks;
    // }

    // updateTaskStatus(id: string, status: TasksStatus): Task {
    //     console.log('updateTaskStatus(id=%s, status=%o)', id, status);

    //     ////1st try
    //     //const idx = this.tasks.findIndex( elem => elem.id === id);
    //     //this.tasks[idx].status = status;
    //     //return this.tasks[idx];

    //     //2nd try, reuse getTaskById
    //     const task = this.getTaskById(id);
    //     task.status = status;
    //     return task;
    // }

    // createTask(createTaskDto: CreateTaskDto): Task {
    //     const {title, description } = createTaskDto;

    //     const task: Task = {
    //         id: uuid(),
    //         title,
    //         description,
    //         status: TasksStatus.OPEN,
    //     };

    //     console.log('service creating task', task);
    //     this.tasks.push(task);
    //     return task;
    // }
}
