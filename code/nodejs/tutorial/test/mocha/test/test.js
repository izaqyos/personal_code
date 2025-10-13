const assert = require('assert');
describe('Array', function () {
  describe('#indexOf()', function () {
      it('should return -1 when the value is not present', function () {
          assert.equal([1, 2, 3].indexOf(4), -1);
      });

      it('double done', function (done) {
          // Calling `done()` twice is an error
          setImmediate(done);
          setImmediate(done);
      });
  });
});

function mult(args) {
    return args.reduce(( prv, cur) => prv*cur, 1);
}

describe('test mult function', function() {
    const test_inputs_outputs = [
        {args: [1,2,3], expected: 6},
        {args: [], expected: 1},
        {args: [-1,2,3], expected: -6},
        {args: [3], expected: 3},
        {args: [1,2,3,4,5,6], expected: 720},
        {args: [1,2,3,4], expected: 24}
    ];

    test_inputs_outputs.forEach(({args, expected}) => {
        it(`test multiplication of ${args}, should be ${expected}`, function() {
            const result = mult(args);
            assert.strictEqual(result, expected);
        });
    });
});

describe('inline-diff demo', function() {
    it('test inline-diff', function() {
        const expected = {
            name: 'yosi',
            surname: 'izaq'
        };
        assert.strictEqual(expected, {
            name: 'yosii',
            surname: 'itzak'
        });
    });
});

describe('test slow function', async function() {
    this.slow(60000); // 1 minute. so >1 slow, 30-60 seconds normal, <30 fast 
   
    it('fast test < 30sec', async function() {
        setTimeout(() => {console.log('fast action');}, 5000);
        //await new Promise(res => setTimeout(res, 5000));
        //done()
    }).timeout(70000);
    it('normal test 60> test time > 30sec', async function(done) {
        console.log('normal test will give error:  Error: Resolution method is overspecified. Specify a callback *or* return a Promise; not both. Reason async function returns promise and done() is another promise');
        await new Promise(res => setTimeout(res, 35000));
        done()
     }).timeout(70000);
    it('slow test > 60sec', async function() {
        setTimeout(() => {console.log('fast action');}, 61000);
    }).timeout(70000);
});

