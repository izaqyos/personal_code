import { Test } from '@nestjs/testing';
import { TasksService } from './tasks.service';
import { TaskRepository } from './task.repository';
import { Module, NotFoundException } from '@nestjs/common';
import { async } from 'rxjs/internal/scheduler/async';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { TaskStatus } from './task-status.enum';
import { CreateTaskDto } from './dto/create-task.dto';

const mockUser = { id: 10, username: 'yosi'};

const mockTaskRepository = () => ({
    getTasks: jest.fn(),
    findOne: jest.fn(),
    createTask: jest.fn(),
});

describe('TaskService', () => {

    let tasksService;
    let taskRepository;

    beforeEach(async () => {
        const module = await Test.createTestingModule({
            providers: [
                TasksService,
                {provide: TaskRepository, useFactory: mockTaskRepository},
            ],
        }).compile();

        tasksService = await module.get<TasksService>(TasksService);
        taskRepository = await module.get<TaskRepository>(TaskRepository);
    });

    describe('getTasks', () => {

        it('gets all tasks from repo', async () => {
            expect(taskRepository.getTasks).not.toHaveBeenCalled();

            taskRepository.getTasks.mockResolvedValue('value');

            const filters: GetTasksFilterDto = { status: TaskStatus.IN_PROGRESS, search: 'Some search query'};
            const res = await tasksService.getTasks(filters, mockUser);
            expect(taskRepository.getTasks).toHaveBeenCalled();
            expect(res).toEqual('value');
        });
    });

    describe('getTaskById', () => {

        it('call taskRepository.findOne() and succesffuly returns task', async () => {
            const mockTask = {title: 'test task', description: 'test task description'};
            taskRepository.findOne.mockResolvedValue(mockTask);

            const res = await tasksService.getTaskById(1, mockUser);
            expect(taskRepository.findOne).toHaveBeenCalledWith({
                where: {
                id: 1,
                userId: mockUser.id,
            },
        });
            expect(res).toEqual(mockTask);
        });

        it('throws error when task not found', async () => {
            taskRepository.findOne.mockResolvedValue(null);
            expect(tasksService.getTaskById(1,mockUser)).rejects.toThrow(NotFoundException);
        });


    });

    describe('createTask tests', () => {
        it('Should call taskRepository.createTask() succesfuly and return the task', async () => {
            const createDto: CreateTaskDto = { title: 'a task', description: 'a desc' };
            const mockTask = {title: 'test task', description: 'test task description'};
            taskRepository.createTask.mockResolvedValue( mockTask );

            const res = await tasksService.createTask(createDto, mockUser);
            expect(taskRepository.createTask).toHaveBeenCalledWith(createDto, mockUser);
            expect(res).toEqual(mockTask);
        });

    });
    
});
