#!/bin/bash
set -euo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/find-disk-images.sh"

fail() { echo "FAIL: $*" >&2; exit 1; }

assert_contains() {
  local haystack="$1"; local needle="$2"
  if ! grep -F -q -- "$needle" <<< "$haystack"; then
    fail "Expected to contain: $needle"
  fi
}

assert_not_contains() {
  local haystack="$1"; local needle="$2"
  if grep -F -q -- "$needle" <<< "$haystack"; then
    fail "Did not expect to contain: $needle"
  fi
}

tmpdir=$(mktemp -d)
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT

mkdir -p "$tmpdir/.Spotlight-V100" "$tmpdir/.Trashes" "$tmpdir/.fseventsd" "$tmpdir/Backups.backupdb"

# Top-level images
touch "$tmpdir/sample.dmg"
touch "$tmpdir/sample.sparseimage"
touch "$tmpdir/sample.img"
touch "$tmpdir/sample.iso"
touch "$tmpdir/sample.cdr"
touch "$tmpdir/sample.qcow2"
touch "$tmpdir/sample.vdi"
touch "$tmpdir/sample.vmdk"
mkdir -p "$tmpdir/test.sparsebundle"

# Images in pruned dirs (should not appear)
touch "$tmpdir/.Spotlight-V100/hidden.dmg"
touch "$tmpdir/.Trashes/hidden.sparseimage"
touch "$tmpdir/.fseventsd/hidden.iso"
touch "$tmpdir/Backups.backupdb/hidden.vmdk"

# Deep nested image
mkdir -p "$tmpdir/level1/level2"
touch "$tmpdir/level1/level2/deep.dmg"

# Non-images
touch "$tmpdir/notes.txt"
touch "$tmpdir/test.sparsebundle.txt"

echo "CASE 1: basic search (no Spotlight)"
out1=$("$SCRIPT" --no-spotlight "$tmpdir")
assert_contains "$out1" "$tmpdir/sample.dmg"
assert_contains "$out1" "$tmpdir/test.sparsebundle"
assert_contains "$out1" "$tmpdir/sample.vmdk"
assert_contains "$out1" "$tmpdir/level1/level2/deep.dmg"
assert_not_contains "$out1" "$tmpdir/.Spotlight-V100/hidden.dmg"
assert_not_contains "$out1" "$tmpdir/Backups.backupdb/hidden.vmdk"
assert_not_contains "$out1" "$tmpdir/notes.txt"
assert_not_contains "$out1" "$tmpdir/test.sparsebundle.txt"

echo "CASE 2: depth limited search (-d 1)"
out2=$("$SCRIPT" --no-spotlight -d 1 "$tmpdir")
assert_contains "$out2" "$tmpdir/sample.dmg"
assert_not_contains "$out2" "$tmpdir/level1/level2/deep.dmg"

echo "CASE 3: nonexistent root should exit 2"
if "$SCRIPT" --no-spotlight "$tmpdir/does-not-exist" >/dev/null 2>&1; then
  fail "Expected failure for nonexistent directory"
else
  code=$?
  [[ $code -eq 2 ]] || fail "Expected exit code 2, got $code"
fi

echo "CASE 4: empty directory should exit 1"
emptydir=$(mktemp -d)
if "$SCRIPT" --no-spotlight "$emptydir" >/dev/null 2>&1; then
  fail "Expected failure for empty directory"
else
  code=$?
  [[ $code -eq 1 ]] || fail "Expected exit code 1, got $code"
fi
rm -rf "$emptydir"

echo "All tests passed."


