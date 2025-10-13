import test from 'node:test';
import assert from 'node:assert/strict';
import {getJsonFromUrl} from './fetch.mjs';

test('Standalone Test fetch positive', async (t) => {
    const url = 'https://jsonplaceholder.typicode.com/todos/1'
    const expected = {
        userId: 1,
        id: 1,
        title: "delectus aut autem",
        completed: false
    };
    const data = await getJsonFromUrl(url);
    assert.deepStrictEqual(data, expected);
});

test('Nested Tests, fetch negatives', async (t) => {
    await t.test('Fetch null url', async (t) => {
        const url = null;
        await assert.rejects(
            getJsonFromUrl(url),
            err => {
                console.log(`got error ${err.name}, message ${err.message}`); // would print got error TypeError, message Failed to parse URL from null
                //assert.strictEqual(err.name, 'TypeError');
                //assert.strictEqual(err.message, 'Failed to parse URL from null');
                return true;
            }
        );
    });
    await t.test('Fetch wrong url', async (t) => {
        const url =  'https://jsonplaceholder.typicode.com/todos/nonexistent';
        await assert.rejects(
            getJsonFromUrl(url),
            err => {
                console.log(`got error ${err.name}, message ${err.message}`); // would print got error TypeError, message Failed to parse URL from null
                assert.equal(err.name, 'Error');
                assert.equal(err.message, 'Got error 404 Not Found');
                return true;
            }
        );
    });
});
