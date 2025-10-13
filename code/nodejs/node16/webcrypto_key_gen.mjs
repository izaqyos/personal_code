// non esm module syntax:
//const { subtle, getRandomValues } = require('crypto').webcrypto;

// esm module syntax:
import { webcrypto } from 'crypto'
const { subtle } = webcrypto;

const getAESKey = async function generateKey(length) {
  return subtle.generateKey(
    { name: 'AES-CBC', length: 256 },
    true,
    ['encrypt', 'decrypt'])};

const aesKey = await getAESKey();
console.log('Generated AES Cipher Block Chaining key', aesKey);




