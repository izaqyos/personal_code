import { Module } from '@nestjs/common';
import { MyservService } from './myserv/myserv.service';

@Module({
  providers: [MyservService]
})
export class MymoduleModule {}
