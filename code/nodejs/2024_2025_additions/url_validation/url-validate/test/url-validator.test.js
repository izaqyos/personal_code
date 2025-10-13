// test/url-validator.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateUrl } from '../url-validator.js';

test('accepts a normal https URL and punycodes', async () => {
  const r = await validateUrl('https://bücher.de/path?q=1', { requireResolvable: false });
  assert.equal(r.ok, true, r.errors?.join('; '));
  assert.equal(r.host, 'xn--bcher-kva.de'); // punycoded
  assert.match(r.normalized, /^https:\/\/xn--bcher-kva\.de\/path\?q=1/);
});

test('allows http if whitelisted', async () => {
  const r = await validateUrl('http://example.com', { requireResolvable: false });
  assert.equal(r.ok, true, r.errors?.join('; '));
});

test('rejects unknown scheme', async () => {
  const r = await validateUrl('javascript:alert(1)');
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /scheme/i.test(e)));
});

test('rejects credentials in URL', async () => {
  const r = await validateUrl('https://user:pass@example.com/');
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /credentials/i.test(e)));
});

test('rejects localhost by name', async () => {
  const r = await validateUrl('http://localhost:8080/', { requireResolvable: false });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /localhost/i.test(e)));
});

test('rejects IPv4 loopback literal', async () => {
  const r = await validateUrl('http://127.0.0.1/', { requireResolvable: false });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /IP denied/i.test(e)));
});

test('rejects IPv6 loopback literal', async () => {
  const r = await validateUrl('http://[::1]/', { requireResolvable: false });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /IP denied/i.test(e)));
});

test('rejects link-local metadata address', async () => {
  const r = await validateUrl('http://169.254.169.254/latest/meta-data', { requireResolvable: false });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /IP denied/i.test(e)));
});

test('rejects IPv6 ULA (private) literal', async () => {
  const r = await validateUrl('http://[fc00::1]/', { requireResolvable: false });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /IP denied/i.test(e)));
});

test('handles non-resolving host when required', async () => {
  const r = await validateUrl('https://nonexistent.example.invalid', { requireResolvable: true });
  assert.equal(r.ok, false);
  assert.ok(r.errors.some(e => /does not resolve/i.test(e)));
});

test('permits non-resolving host when not required', async () => {
  const r = await validateUrl('https://nonexistent.example.invalid', { requireResolvable: false });
  // Should pass syntax/scheme/userinfo/punycode checks; DNS resolution is skipped as a hard requirement
  assert.equal(r.ok, true, r.errors?.join('; '));
});
