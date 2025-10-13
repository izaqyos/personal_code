describe("promises", function () {
    var assert = require('assert'),
        sinon = require('sinon'),
        Q = require('q');

    function doSomeAsync(val) {return Q.resolve(val);}

    var calc = {
        addAsync: function (a, b) {
            return Q.Promise(function (resolve, reject) {
                process.nextTick(function () {
                    resolve(a + b);
                });
            });
        }
    };

    // TODO: Fix the test so it will FAIL on assertion (not on timeout)
    it('error handling', function (done) {
        doSomeAsync()
        ///// write your code below /////
            .then(function (result) {
                assert.ok(result); // result == undefined
                done();
            });
    });

    // TODO: complete multiple calls to promise and make this test green:
    // call to calc.addAsync(x, offset)
    // where x is the values of 0...n
    // do the following assertions:
    //     sinon.assert.callCount(calc.addAsync, n);
    //     assert.equal(results.length, n);
    // don't forget to clean:
    //     calc.addAsync.restore();
    //     done();
    it('multiple calls', function (done) {
        sinon.spy(calc, "addAsync");
        var n = 100;
        var offset = 10;
        ///// write your code below /////
    });

});