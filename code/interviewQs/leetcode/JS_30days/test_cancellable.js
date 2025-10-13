const { expect } = require('chai');
const cancellable = require('./cancellable');

describe('cancellable', () => {

    it('should execute fn after delay if not cancelled', () => {
        const fn = x => x * 2;
        const args = [3];
        const delay = 10;

        const cancelFn = cancellable(fn, args, delay);

        setTimeout(() => {
            expect(fn(...args)).to.equal(6);
        }, delay + 5);
    });

    it('should not execute fn if cancelled before delay', () => {
        const fn = () => {
            throw new Error('Fn executed!');
        };
        const args = [];
        const delay = 100;

        const cancelFn = cancellable(fn, args, delay);
        cancelFn();

        setTimeout(() => { }, delay + 5);
    });

    it('should pass multiple args to fn', () => {
        const fn = (x, y) => x * y;
        const args = [2, 5];
        const delay = 20;

        const cancelFn = cancellable(fn, args, delay);

        setTimeout(() => {
            expect(fn(...args)).to.equal(10);
        }, delay + 5);
    });

});
