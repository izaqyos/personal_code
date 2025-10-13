import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MymoduleModule } from './mymodule/mymodule.module';

@Module({
  imports: [MymoduleModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
