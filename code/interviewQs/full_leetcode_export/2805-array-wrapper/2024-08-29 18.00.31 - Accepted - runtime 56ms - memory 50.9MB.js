var ArrayWrapper = function (nums) {
  this.nums = nums;
  console.log(`CTOR called. got ${nums}, set ${this.nums}`);
};

/**
 * @return {number}
 */
ArrayWrapper.prototype.valueOf = function () {
  return this.nums.reduce((totalsum, num) => totalsum + num, 0);
  console.log(`valueOf called. nums =  ${this.nums}`);
};

/**
 * @return {string}
 */
ArrayWrapper.prototype.toString = function () {
  console.log(this.nums);
  return JSON.stringify(this.nums);
};