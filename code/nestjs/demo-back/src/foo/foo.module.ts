import { Module } from '@nestjs/common';
import { FooController } from './foo.controller';
import { FooService } from './foo.service';

@Module({
  controllers: [FooController],
  providers: [FooService]
})
export class FooModule {}
