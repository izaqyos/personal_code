import { Controller, Post, Body, ValidationPipe, UseGuards, Req, Logger } from '@nestjs/common';
import { AuthCredentialsDto } from './dto/auth-credentials.dto';
import { AuthService } from './auth.service';
import { AuthGuard } from '@nestjs/passport';
import { GetUser } from './get-user.decorator';
import { User } from './user.entity';

@Controller('auth')
export class AuthController {
  private logger = new Logger('auth.controller');

  constructor(
    private authService: AuthService,
  ) {
    this.logger.verbose('CTOR called');
  }

  @Post('/signup')
  signUp(@Body(ValidationPipe) authCredentialsDto: AuthCredentialsDto): Promise<void> {
    this.logger.verbose(`signup called with ${authCredentialsDto}`);
    return this.authService.signUp(authCredentialsDto);
  }

  @Post('/signin')
  signIn(@Body(ValidationPipe) authCredentialsDto: AuthCredentialsDto): Promise<{ accessToken: string }> {
    this.logger.verbose(`signin called with ${authCredentialsDto}`);
    return this.authService.signIn(authCredentialsDto);
  }

  @Post('/test')
  @UseGuards(AuthGuard())
  // test(@Req() req) { //get full req
  test(@GetUser() user: User) {
    //Flow is. a- signup, b- signin get access token, copy value, c- /auth/test w/ 'Authorization' header, value Bearer <paste token>
    // console.log('/test. got request ', req);
    this.logger.verbose(`auth/test called with user ${user}`);
  }
}
