import { webcrypto } from 'crypto';
const { subtle } = webcrypto;
 
(async function() {
  const key = await subtle.generateKey({
    name: 'HMAC',
    hash: 'SHA-256',
    length: 256
  }, true, ['sign', 'verify']);
 
  const digest = await subtle.sign({
    name: 'HMAC'
  }, key, 'foo bar');
 
  console.log(digest);
})();

