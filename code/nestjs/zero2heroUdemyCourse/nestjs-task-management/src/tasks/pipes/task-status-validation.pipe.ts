import { PipeTransform, ValidationPipe, ArgumentMetadata, BadRequestException } from '@nestjs/common';
//import { TasksStatus } from '../tasks.model';
import { TaskStatus } from '../task-status.enum';

export class TaskStatusValidationPipe implements PipeTransform {
    readonly allowedStatuses = [
        TaskStatus.OPEN,
        TaskStatus.IN_PROGRESS,
        TaskStatus.DONE,
    ];

    private isStatusValid(status: any): boolean {
        return (this.allowedStatuses.indexOf(status) !== -1) ;
    }

    transform(value: any, metadata: ArgumentMetadata) {
        console.log(`value=${value}, metadata=${metadata}`);

        if (! this.isStatusValid(value.toUpperCase()) ) {
            throw new BadRequestException(`status ${value} is not valid`);
        }
        return value;
    }
}