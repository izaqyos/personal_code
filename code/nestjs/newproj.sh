#setup 
brew install node
npm i -g @nestjs/cli

# git repo: https://github.com/izaqyos/nestjs101
# branch: initial_setup
nest n demo
rm demo/src/app.controller.spec.ts
rm demo/src/app.service.ts
rm demo/src/app.controller.ts
cp ~/temp/tsconfig.json .
cp ~/temp/package.json .

# remove refs in app.module
# update package.json and tsconfig

#branch: firstModule
cd demo
nest g mo foo
nest g co foo --no-spec
nest g s foo --no-spec
#inject foo service to controller
#demo db in memory. add to foo service.
#wireup get all in controller, @Get()
#test 
curl http://localhost:3000/foo



#branch create_foo
#create foo model. modify get to return foo type
#add a createFoo method. install uuid for ids. import {v1 as uuidv1} from 'uuid';
#in controller add a Post method for creation. just get and print body at first
# Test. postman or curl:
curl --location --request POST 'http://localhost:3000/foo' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'title=new foo'


#branch create_foo_2
#chg controller, create take params, not body. then call service to crete foo
#create a few tasks. the call get to show them

#branch create_foo_3
#now add a DTO. chg controller to use it
#create a few tasks. the call get to show them

#branch foo_crud
#add get by id @Get(':id'), create foo and get by id (@Param('id')) use array.find(elem => predicate)
#add delete by id @Delete(':id'), create foo and delete by id (@Param('id')).  use array.findIndex(elem => predicate), then splice index,1
curl --location --request DELETE 'http://localhost:3000/foo/<id>'

#patch request to update state
curl --location --request PATCH 'http://localhost:3000/foo/9a20cc40-0ef1-11eb-a5ed-a99485c02b39/state' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'state=WIP'

#for patch add @Patch(':id/state') update(@Param('id')..., @Body('state') state: FooState)
#in service updateById method.  get foo by id and chg state. return foo...

#branch validationPipe
npm i class-validator class-transformer --save    
#show that u can create w/ empty title. then add @IsNotEmpty() to DTO title.  and add @UsePipes(ValidationPipe)
#send empty title again. show error. 


