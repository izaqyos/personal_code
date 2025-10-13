import { Module } from '@nestjs/common';
import { FooModule } from './foo/foo.module';

@Module({
  imports: [FooModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
