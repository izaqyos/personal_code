Language notes (Node.js / TypeScript / NestJS): TypeScript strict, no `any`, no non-null `!` to silence the
compiler; async/await, never mix in raw callbacks; always await or return promises (no floating promises);
throw Error subclasses; use the repo's test runner (Jest, Vitest or node:test) and its `it`/`test` titles as
written in the test plan. NestJS: inject through constructors, keep controllers thin and logic in providers,
validate input with DTOs and class-validator, throw Nest HttpExceptions at the edge only, test providers with
Test.createTestingModule and mock only the boundaries.
