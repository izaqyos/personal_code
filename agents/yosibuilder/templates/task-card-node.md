id: N1
title: feat(users): find a user by email
lang: nestjs
edit: src/users/users.service.ts src/users/users.service.spec.ts
read: src/users/user.entity.ts src/users/users.repository.ts
test: npx jest src/users/users.service.spec.ts --ci
lint: npx tsc --noEmit -p tsconfig.json && npx eslint src/users
---
Goal: UsersService.findByEmail returns the user for a known email and throws NotFoundException otherwise.

## Design (implement exactly these, nothing more)

File src/users/users.service.ts:

    @Injectable() export class UsersService
        constructor(private readonly users: UsersRepository)
        async findByEmail(email: string): Promise<User>
            Normalise with email.trim().toLowerCase(); look up with this.users.findOneByEmail;
            throw new NotFoundException(`no user ${email}`) when it returns null.

## Test plan (write exactly these tests in src/users/users.service.spec.ts)

Build the service with Test.createTestingModule and a stub UsersRepository.

it("returns the user for a known email")
it("normalises case and whitespace before the lookup")
it("throws NotFoundException for an unknown email")

Constraints: no comments, no other files, functions about 20 lines or fewer, no `any`.
