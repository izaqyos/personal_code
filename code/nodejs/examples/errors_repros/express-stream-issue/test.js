// test.js
const request = require('supertest');
const streamEqual = require('stream-equal'); // Used for buffer comparison if needed

// Import servers - IMPORTANT: ensure they export the server instance
let serverError;
let serverFixed;

// Use Jest's lifecycle hooks
beforeAll(() => {
    // Dynamically require servers inside beforeAll to ensure fresh instances if tests re-run
    serverError = require('./server-error');
    serverFixed = require('./server-fixed');
});

afterAll((done) => {
    // Close servers after tests
    serverError.close(() => {
        serverFixed.close(done);
    });
});


describe('Express Stream Conflict Simulation', () => {

    const testPayload = { message: 'hello world', value: 123 };

    // Test the server that demonstrates the error
    describe('Error Server (server-error.js)', () => {
        it('should fail with 500 due to stream conflict', async () => {
            const response = await request(serverError)
               .post('/test')
               .send(testPayload)
               .set('Content-Type', 'application/json')
               .set('Accept', 'application/json');

            // Expect the 500 error sent by our simulated conflictMiddleware
            expect(response.status).toBe(500);
            expect(response.text).toContain('Internal Server Error: Stream conflict (simulated)');
        });
         it('should fail with 500 even with empty payload', async () => {
            // Test edge case: empty JSON object still triggers parsing
            const response = await request(serverError)
               .post('/test')
               .send({})
               .set('Content-Type', 'application/json')
               .set('Accept', 'application/json');

            expect(response.status).toBe(500);
            expect(response.text).toContain('Internal Server Error: Stream conflict (simulated)');
        });
    });

    // Test the server with the buffering middleware fix
    describe('Fixed Server (server-fixed.js)', () => {
        it('should succeed and return the parsed body', async () => {
            const response = await request(serverFixed)
               .post('/test')
               .send(testPayload)
               .set('Content-Type', 'application/json')
               .set('Accept', 'application/json');

            expect(response.status).toBe(200);
            expect(response.body.message).toBe('Success (Fixed Server)');
            expect(response.body.receivedBody).toEqual(testPayload);
            // Check if the conflict middleware also read the same data
            expect(response.body.conflictReadMatches).toBe(true);
        });

         it('should succeed with empty payload', async () => {
            const response = await request(serverFixed)
               .post('/test')
               .send({})
               .set('Content-Type', 'application/json')
               .set('Accept', 'application/json');

            expect(response.status).toBe(200);
            expect(response.body.message).toBe('Success (Fixed Server)');
            expect(response.body.receivedBody).toEqual({});
            expect(response.body.conflictReadMatches).toBe(true);
        });

         it('should handle larger payloads within limit', async () => {
            const largePayload = { data: 'a'.repeat(100 * 1024) }; // 100KB string
            const response = await request(serverFixed)
               .post('/test')
               .send(largePayload)
               .set('Content-Type', 'application/json')
               .set('Accept', 'application/json');

            expect(response.status).toBe(200);
            expect(response.body.message).toBe('Success (Fixed Server)');
            expect(response.body.receivedBody.data.length).toBe(100 * 1024);
            expect(response.body.conflictReadMatches).toBe(true);
        });

         it('should reject payloads exceeding the limit (413)', async () => {
             // Payload slightly larger than the 1mb limit in bufferRawBodyMiddleware
             const tooLargePayload = { data: 'a'.repeat(1.1 * 1024 * 1024) };
             const response = await request(serverFixed)
                .post('/test')
                .send(tooLargePayload)
                .set('Content-Type', 'application/json')
                .set('Accept', 'application/json');

             // Expect 413 from the buffering middleware's error handling
             expect(response.status).toBe(413);
             expect(response.text).toBe('Payload Too Large');
         });
    });
});
