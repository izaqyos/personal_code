import { Test, TestingModule } from '@nestjs/testing';
import { MyservService } from './myserv.service';

describe('MyservService', () => {
  let service: MyservService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [MyservService],
    }).compile();

    service = module.get<MyservService>(MyservService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
